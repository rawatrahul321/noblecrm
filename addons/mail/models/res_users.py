# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import _, api, exceptions, fields, models, modules
from noblecrm.tools import pycompat
from noblecrm.addons.base.res.res_users import is_selection_groups


class Users(models.Model):
    """ Update of res.users class
        - add a preference about sending emails about notifications
        - make a new user follow itself
        - add a welcome message
        - add suggestion preference
        - if adding groups to an user, check mail.channels linked to this user
          group, and the user. This is done by overriding the write method.
    """
    _name = 'res.users'
    _inherit = ['res.users']

    alias_id = fields.Many2one('mail.alias', 'Alias', ondelete="set null", required=False,
            help="Email address internally associated with this user. Incoming "\
                 "emails will appear in the user's notifications.", copy=False, auto_join=True)
    alias_contact = fields.Selection([
        ('everyone', 'Everyone'),
        ('partners', 'Authenticated Partners'),
        ('followers', 'Followers only')], string='Alias Contact Security', related='alias_id.alias_contact')
    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in NobleCRM')],
        'Notification Management', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Emails: notifications are sent to your email\n"
             "- NobleCRM: notifications appear in your NobleCRM Inbox")

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(Users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['notification_type'])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['notification_type'])
        return init_res

    @api.model
    def create(self, values):
        if not values.get('login', False):
            action = self.env.ref('base.action_res_users')
            msg = _("You cannot create a new user from here.\n To create new user please go to configuration panel.")
            raise exceptions.RedirectWarning(msg, action.id, _('Go to the configuration panel'))

        user = super(Users, self).create(values)

        # create a welcome message
        user._create_welcome_message()
        # Auto-subscribe to channels
        self.env['mail.channel'].search([('group_ids', 'in', user.groups_id.ids)])._subscribe_users()
        return user

    @api.multi
    def write(self, vals):
        write_res = super(Users, self).write(vals)
        sel_groups = [vals[k] for k in vals if is_selection_groups(k) and vals[k]]
        if vals.get('groups_id'):
            # form: {'group_ids': [(3, 10), (3, 3), (4, 10), (4, 3)]} or {'group_ids': [(6, 0, [ids]}
            user_group_ids = [command[1] for command in vals['groups_id'] if command[0] == 4]
            user_group_ids += [id for command in vals['groups_id'] if command[0] == 6 for id in command[2]]
            self.env['mail.channel'].search([('group_ids', 'in', user_group_ids)])._subscribe_users()
        elif sel_groups:
            self.env['mail.channel'].search([('group_ids', 'in', sel_groups)])._subscribe_users()
        return write_res

    def _create_welcome_message(self):
        self.ensure_one()
        if not self.has_group('base.group_user'):
            return False
        company_name = self.company_id.name if self.company_id else ''
        body = _('%s has joined the %s network.') % (self.name, company_name)
        # TODO change SUPERUSER_ID into user.id but catch errors
        return self.partner_id.sudo().message_post(body=body)

    def _message_post_get_pid(self):
        self.ensure_one()
        if 'thread_model' in self.env.context:
            self = self.with_context(thread_model='res.users')
        return self.partner_id.id

    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, **kwargs):
        """ Redirect the posting of message on res.users as a private discussion.
            This is done because when giving the context of Chatter on the
            various mailboxes, we do not have access to the current partner_id. """
        current_pids = []
        partner_ids = kwargs.get('partner_ids', [])
        user_pid = self._message_post_get_pid()
        for partner_id in partner_ids:
            if isinstance(partner_id, (list, tuple)) and partner_id[0] == 4 and len(partner_id) == 2:
                current_pids.append(partner_id[1])
            elif isinstance(partner_id, (list, tuple)) and partner_id[0] == 6 and len(partner_id) == 3:
                current_pids.append(partner_id[2])
            elif isinstance(partner_id, pycompat.integer_types):
                current_pids.append(partner_id)
        if user_pid not in current_pids:
            partner_ids.append(user_pid)
        kwargs['partner_ids'] = partner_ids
        return self.env['mail.thread'].message_post(**kwargs)

    def message_update(self, msg_dict, update_vals=None):
        return True

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None, force=True):
        return True

    @api.multi
    def message_partner_info_from_emails(self, emails, link_mail=False):
        return self.env['mail.thread'].message_partner_info_from_emails(emails, link_mail=link_mail)

    @api.multi
    def message_get_suggested_recipients(self):
        return dict((res_id, list()) for res_id in self._ids)

    @api.model
    def activity_user_count(self):
        query = """SELECT m.id, count(*), act.res_model as model,
                        CASE
                            WHEN %(today)s::date - act.date_deadline::date = 0 Then 'today'
                            WHEN %(today)s::date - act.date_deadline::date > 0 Then 'overdue'
                            WHEN %(today)s::date - act.date_deadline::date < 0 Then 'planned'
                        END AS states
                    FROM mail_activity AS act
                    JOIN ir_model AS m ON act.res_model_id = m.id
                    WHERE user_id = %(user_id)s
                    GROUP BY m.id, states, act.res_model;
                    """
        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid,
        })
        activity_data = self.env.cr.dictfetchall()
        model_ids = [a['id'] for a in activity_data]
        model_names = {n[0]:n[1] for n in self.env['ir.model'].browse(model_ids).name_get()}

        user_activities = {}
        for activity in activity_data:
            if not user_activities.get(activity['model']):
                user_activities[activity['model']] = {
                    'name': model_names[activity['id']],
                    'model': activity['model'],
                    'icon': modules.module.get_module_icon(self.env[activity['model']]._original_module),
                    'total_count': 0, 'today_count': 0, 'overdue_count': 0, 'planned_count': 0,
                }
            user_activities[activity['model']]['%s_count' % activity['states']] += activity['count']
            if activity['states'] in ('today','overdue'):
                user_activities[activity['model']]['total_count'] += activity['count']

        return list(user_activities.values())


class res_groups_mail_channel(models.Model):
    """ Update of res.groups class
        - if adding users from a group, check mail.channels linked to this user
          group and subscribe them. This is done by overriding the write method.
    """
    _name = 'res.groups'
    _inherit = 'res.groups'

    @api.multi
    def write(self, vals, context=None):
        write_res = super(res_groups_mail_channel, self).write(vals)
        if vals.get('users'):
            # form: {'group_ids': [(3, 10), (3, 3), (4, 10), (4, 3)]} or {'group_ids': [(6, 0, [ids]}
            user_ids = [command[1] for command in vals['users'] if command[0] == 4]
            user_ids += [id for command in vals['users'] if command[0] == 6 for id in command[2]]
            self.env['mail.channel'].search([('group_ids', 'in', self._ids)])._subscribe_users()
        return write_res
