# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
import base64
import logging

from noblecrm import api, fields, models
from noblecrm import tools, _
from noblecrm.exceptions import ValidationError, AccessError
from noblecrm.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class EmployeeCategory(models.Model):

    _name = "hr.employee.category"
    _description = "Employee Category"

    name = fields.Char(string="Employee Tag", required=True)
    color = fields.Integer(string='Color Index')
    employee_ids = fields.Many2many('hr.employee', 'employee_category_rel', 'category_id', 'emp_id', string='Employees')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class Job(models.Model):

    _name = "hr.job"
    _description = "Job Position"
    _inherit = ['mail.thread']

    name = fields.Char(string='Job Position', required=True, index=True, translate=True)
    expected_employees = fields.Integer(compute='_compute_employees', string='Total Forecasted Employees', store=True,
        help='Expected number of employees for this job position after new recruitment.')
    no_of_employee = fields.Integer(compute='_compute_employees', string="Current Number of Employees", store=True,
        help='Number of employees currently occupying this job position.')
    no_of_recruitment = fields.Integer(string='Expected New Employees', copy=False,
        help='Number of new employees you expect to recruit.', default=1)
    no_of_hired_employee = fields.Integer(string='Hired Employees', copy=False,
        help='Number of hired employees for this job position during recruitment phase.')
    employee_ids = fields.One2many('hr.employee', 'job_id', string='Employees', groups='base.group_user')
    description = fields.Text(string='Job Description')
    requirements = fields.Text('Requirements')
    department_id = fields.Many2one('hr.department', string='Department')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    state = fields.Selection([
        ('recruit', 'Recruitment in Progress'),
        ('open', 'Not Recruiting')
    ], string='Status', readonly=True, required=True, track_visibility='always', copy=False, default='recruit', help="Set whether the recruitment process is open or closed for this job position.")

    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id, department_id)', 'The name of the job position must be unique per department in company!'),
    ]

    @api.depends('no_of_recruitment', 'employee_ids.job_id', 'employee_ids.active')
    def _compute_employees(self):
        employee_data = self.env['hr.employee'].read_group([('job_id', 'in', self.ids)], ['job_id'], ['job_id'])
        result = dict((data['job_id'][0], data['job_id_count']) for data in employee_data)
        for job in self:
            job.no_of_employee = result.get(job.id, 0)
            job.expected_employees = result.get(job.id, 0) + job.no_of_recruitment

    @api.model
    def create(self, values):
        """ We don't want the current user to be follower of all created job """
        return super(Job, self.with_context(mail_create_nosubscribe=True)).create(values)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        return super(Job, self).copy(default=default)

    @api.multi
    def set_recruit(self):
        for record in self:
            no_of_recruitment = 1 if record.no_of_recruitment == 0 else record.no_of_recruitment
            record.write({'state': 'recruit', 'no_of_recruitment': no_of_recruitment})
        return True

    @api.multi
    def set_open(self):
        return self.write({
            'state': 'open',
            'no_of_recruitment': 0,
            'no_of_hired_employee': 0
        })


class Employee(models.Model):
    _name = "hr.employee"
    _description = "Employee"
    _order = 'name'
    _inherit = ['mail.thread', 'resource.mixin']

    _mail_post_access = 'read'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    # resource and user
    # required on the resource, make sure required="True" set in the view
    name = fields.Char(related='resource_id.name', store=True, oldname='name_related')
    user_id = fields.Many2one('res.users', 'User', related='resource_id.user_id')
    active = fields.Boolean('Active', related='resource_id.active', default=True, store=True)
    # private partner
    address_home_id = fields.Many2one(
        'res.partner', 'Private Address', help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user")
    is_address_home_a_company = fields.Boolean(
        'The employee adress has a company linked',
        compute='_compute_is_address_home_a_company',
    )
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", default="male")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single')
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user")
    ssnid = fields.Char('SSN No', help='Social Security Number', groups="hr.group_hr_user")
    sinid = fields.Char('SIN No', help='Social Insurance Number', groups="hr.group_hr_user")
    identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user")
    passport_id = fields.Char('Passport No', groups="hr.group_hr_user")
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id)]",
        groups="hr.group_hr_user",
        help='Employee bank salary account')
    permit_no = fields.Char('Work Permit No', groups="hr.group_hr_user")
    visa_no = fields.Char('Visa No', groups="hr.group_hr_user")
    visa_expire = fields.Date('Visa Expire Date', groups="hr.group_hr_user")

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Photo", default=_default_image, attachment=True,
        help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized photo", attachment=True,
        help="Medium-sized photo of the employee. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized photo", attachment=True,
        help="Small-sized photo of the employee. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    # work
    address_id = fields.Many2one(
        'res.partner', 'Work Address')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    work_location = fields.Char('Work Location')
    # employee in company
    job_id = fields.Many2one('hr.job', 'Job Position')
    department_id = fields.Many2one('hr.department', 'Department')
    parent_id = fields.Many2one('hr.employee', 'Manager')
    child_ids = fields.One2many('hr.employee', 'parent_id', string='Subordinates')
    coach_id = fields.Many2one('hr.employee', 'Coach')
    category_ids = fields.Many2many(
        'hr.employee.category', 'employee_category_rel',
        'emp_id', 'category_id',
        string='Tags')
    # misc
    notes = fields.Text('Notes')
    color = fields.Integer('Color Index', default=0)

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for employee in self:
            if not employee._check_recursion():
                raise ValidationError(_('Error! You cannot create recursive hierarchy of Employee(s).'))

    @api.onchange('address_id')
    def _onchange_address(self):
        self.work_phone = self.address_id.phone
        self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('department_id')
    def _onchange_department(self):
        self.parent_id = self.department_id.manager_id

    @api.onchange('user_id')
    def _onchange_user(self):
        if self.user_id:
            self.update(self._sync_user(self.user_id))

    def _sync_user(self, user):
        return dict(
            name=user.name,
            image=user.image,
            work_email=user.email,
        )

    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id'])))
        tools.image_resize_images(vals)
        return super(Employee, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'address_home_id' in vals:
            account_id = vals.get('bank_account_id') or self.bank_account_id.id
            if account_id:
                self.env['res.partner.bank'].browse(account_id).partner_id = vals['address_home_id']
        tools.image_resize_images(vals)
        return super(Employee, self).write(vals)

    @api.multi
    def unlink(self):
        resources = self.mapped('resource_id')
        super(Employee, self).unlink()
        return resources.unlink()

    @api.multi
    def action_follow(self):
        """ Wrapper because message_subscribe_users take a user_ids=None
            that receive the context without the wrapper.
        """
        return self.message_subscribe_users()

    @api.multi
    def action_unfollow(self):
        """ Wrapper because message_unsubscribe_users take a user_ids=None
            that receive the context without the wrapper.
        """
        return self.message_unsubscribe_users()

    @api.model
    def _message_get_auto_subscribe_fields(self, updated_fields, auto_follow_fields=None):
        """ Overwrite of the original method to always follow user_id field,
            even when not track_visibility so that a user will follow it's employee
        """
        if auto_follow_fields is None:
            auto_follow_fields = ['user_id']
        user_field_lst = []
        for name, field in self._fields.items():
            if name in auto_follow_fields and name in updated_fields and field.comodel_name == 'res.users':
                user_field_lst.append(name)
        return user_field_lst

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids):
        # Do not notify user it has been marked as follower of its employee.
        return

    @api.depends('address_home_id.parent_id')
    def _compute_is_address_home_a_company(self):
        """Checks that choosen address (res.partner) is not linked to a company.
        """
        for employee in self:
            try:
                employee.is_address_home_a_company = employee.address_home_id.parent_id.id is not False
            except AccessError:
                employee.is_address_home_a_company = False


class Department(models.Model):
    _name = "hr.department"
    _description = "HR Department"
    _inherit = ['mail.thread']
    _order = "name"
    _rec_name = 'complete_name'

    name = fields.Char('Department Name', required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id)
    parent_id = fields.Many2one('hr.department', string='Parent Department', index=True)
    child_ids = fields.One2many('hr.department', 'parent_id', string='Child Departments')
    manager_id = fields.Many2one('hr.employee', string='Manager', track_visibility='onchange')
    member_ids = fields.One2many('hr.employee', 'department_id', string='Members', readonly=True)
    jobs_ids = fields.One2many('hr.job', 'department_id', string='Jobs')
    note = fields.Text('Note')
    color = fields.Integer('Color Index')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive departments.'))

    @api.model
    def create(self, vals):
        # TDE note: auto-subscription of manager done by hand, because currently
        # the tracking allows to track+subscribe fields linked to a res.user record
        # An update of the limited behavior should come, but not currently done.
        department = super(Department, self.with_context(mail_create_nosubscribe=True)).create(vals)
        manager = self.env['hr.employee'].browse(vals.get("manager_id"))
        if manager.user_id:
            department.message_subscribe_users(user_ids=manager.user_id.ids)
        return department

    @api.multi
    def write(self, vals):
        """ If updating manager of a department, we need to update all the employees
            of department hierarchy, and subscribe the new manager.
        """
        # TDE note: auto-subscription of manager done by hand, because currently
        # the tracking allows to track+subscribe fields linked to a res.user record
        # An update of the limited behavior should come, but not currently done.
        if 'manager_id' in vals:
            manager_id = vals.get("manager_id")
            if manager_id:
                manager = self.env['hr.employee'].browse(manager_id)
                # subscribe the manager user
                if manager.user_id:
                    self.message_subscribe_users(user_ids=manager.user_id.ids)
            # set the employees's parent to the new manager
            self._update_employee_manager(manager_id)
        return super(Department, self).write(vals)

    def _update_employee_manager(self, manager_id):
        employees = self.env['hr.employee']
        for department in self:
            employees = employees | self.env['hr.employee'].search([
                ('id', '!=', manager_id),
                ('department_id', '=', department.id),
                ('parent_id', '=', department.manager_id.id)
            ])
        employees.write({'parent_id': manager_id})
