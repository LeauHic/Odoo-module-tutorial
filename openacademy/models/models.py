# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Courses'

    name = fields.Char(string="Title", required=True, help="Name of the Course")
    description = fields.Text()
    responsible = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    number_of_session = fields.Integer(compute='_number_of_session')
    session_related = fields.One2many('openacademy.session', 'course_related', string="Related sessions")

    @api.depends('session_related')
    def _number_of_session(self):
        for record in self:
            if not record.session_related:
                record.number_of_session = 0
            else:
                record.number_of_session = len(record.session_related)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Session'

    name = fields.Char(string="Session name", required=True)
    active = fields.Boolean(required=True, default=True)
    start_date = fields.Date(required=True, help="Date of the session",
                             default=fields.date.today())
    duration = fields.Float(digits=(6, 2), string="Duration of the session (Days)", required=True)
    end_date = fields.Date(compute="_end_date", help="End of the session", reverse="_set_end_date")
    numberOfSeat = fields.Integer(string="Number of seat available", required=True)
    instructor = fields.Many2one("res.partner", ondelete='set null', index=True,
                                 domain=['|', ('instructor', '=', True), ('teacher', 'ilike', 'Teacher')])
    course_related = fields.Many2one("openacademy.course", ondelete='cascade', string="Related Course", index=True)
    attendee = fields.Many2many("res.partner", string="Attendees")
    taken_seats = fields.Float(compute='_taken_seats')
    color = fields.Integer()

    @api.constrains('instructor', 'attendee')
    def _check_instructor_not_in_attendee(self):
        for r in self:
            if r.instructor and r.instructor in r.attendee:
                raise exceptions.ValidationError("A session's instructor cannot be attendee")

    @api.depends('numberOfSeat', 'attendee')
    def _taken_seats(self):
        for record in self:
            if not record.numberOfSeat:
                record.taken_seats = 0.0
            else:
                record.taken_seats = 100 * len(record.attendee) / record.numberOfSeat

    @api.depends('start_date', 'duration')
    def _end_date(self):
        for record in self:
            if not (record.duration and record.start_date):
                record.end_date = 0
            else:
                record.end_date = record.start_date + datetime.timedelta(record.duration)

    def _set_end_date(self):
        for record in self:
            if not (record.start_date and record.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            record.duration = (record.end_date - record.start_date).days + 1

    @api.onchange('numberOfSeat', 'taken_seats')
    def _verify_valid_seats(self):
        if self.numberOfSeat <= 0:
            self.numberOfSeat = 0
            return {
                'warning': {
                    'title': 'Incorrect seats value',
                    'message': 'A seat value cannot be negative or null',
                }
            }
        if len(self.attendee) > self.numberOfSeat:
            return {
                'warning': {
                    'title': 'All places are taken',
                    'message': 'There is more attendee than available seats',
                }
            }

