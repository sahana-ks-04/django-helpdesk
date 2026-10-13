from django.db import migrations


def add_reopened_email_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")

    templates = {
        "reopened_cc": {
            "heading": "Ticket Reopened",
            "subject": "(Reopened)",
            "locale": "en",
            "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Ticket <a href=\"{{ ticket.staff_url }}\"><b>{{ ticket.ticket }}</b></a> (<em>{{ ticket.title }}</em>){% if ticket.assigned_to %}, assigned to {{ ticket.get_assigned_to }}{% endif %}, has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">\r\n<b>Ticket ID</b>: {{ ticket.ticket }}<br>\r\n<b>Queue</b>: {{ queue.title }}<br>\r\n<b>Title</b>: {{ ticket.title }}<br>\r\n<b>Opened</b>: {{ ticket.created|date:\"DATETIME_FORMAT\" }}<br>\r\n<b>Submitter</b>: {{ ticket.submitter_email|default:\"Unknown\" }}<br>\r\n<b>Priority</b>: {{ ticket.get_priority_display }}<br>\r\n<b>Status</b>: {{ ticket.get_status }}<br>\r\n<b>Assigned to</b>: {{ ticket.get_assigned_to }}<br>\r\n<b><a href='{{ ticket.staff_url }}'>View Online</a></b> to update this ticket (login required)</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Just for reference, the original ticket description was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ ticket.description|linebreaksbr }}</blockquote>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">The latest update was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ resolution }}</blockquote>",
            "plain_text": "Hello,\r\n\r\nTicket {{ ticket.ticket }} (\"{{ ticket.title }}\"){% if ticket.assigned_to %}, assigned to {{ ticket.assigned_to }}{% endif %} has been reopened.\r\n\r\nTicket ID: {{ ticket.ticket }}\r\nQueue: {{ queue.title }}\r\nTitle: {{ ticket.title }}\r\nOpened: {{ ticket.created|date:\"DATETIME_FORMAT\" }}\r\nSubmitter: {{ ticket.submitter_email|default:\"Unknown\" }}\r\nPriority: {{ ticket.get_priority_display }}\r\nStatus: {{ ticket.get_status }}\r\nAssigned to: {{ ticket.get_assigned_to }}\r\nView Online: {{ ticket.staff_url }} (login required)\r\n\r\nThe original description was:\r\n\r\n{{ ticket.description }}\r\n\r\nThe latest update was:\r\n\r\n{{ resolution }}\r\n\r\n",
        },
        "reopened_owner": {
            "heading": "Ticket Reopened",
            "subject": "(Reopened)",
            "locale": "en",
            "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">The following ticket, which is currently assigned to you, has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">\r\n<b>Ticket ID</b>: {{ ticket.ticket }}<br>\r\n<b>Queue</b>: {{ queue.title }}<br>\r\n<b>Title</b>: {{ ticket.title }}<br>\r\n<b>Opened</b>: {{ ticket.created|date:\"DATETIME_FORMAT\" }}<br>\r\n<b>Submitter</b>: {{ ticket.submitter_email|default:\"Unknown\" }}<br>\r\n<b>Priority</b>: {{ ticket.get_priority_display }}<br>\r\n<b>Status</b>: {{ ticket.get_status }}<br>\r\n<b>Assigned to</b>: {{ ticket.get_assigned_to }}<br>\r\n<b><a href='{{ ticket.staff_url }}'>View Online</a></b> to update this ticket (login required)</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Just for reference, the original ticket description was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ ticket.description|linebreaksbr }}</blockquote>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">The latest update was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ resolution }}</blockquote>",
            "plain_text": "Hello,\r\n\r\nThe following ticket, which is currently assigned to you, has been reopened.\r\n\r\nTicket ID: {{ ticket.ticket }}\r\nQueue: {{ queue.title }}\r\nTitle: {{ ticket.title }}\r\nOpened: {{ ticket.created|date:\"DATETIME_FORMAT\" }}\r\nSubmitter: {{ ticket.submitter_email|default:\"Unknown\" }}\r\nPriority: {{ ticket.get_priority_display }}\r\nStatus: {{ ticket.get_status }}\r\nAssigned to: {{ ticket.get_assigned_to }}\r\nView Online: {{ ticket.staff_url }} (login required)\r\n\r\nThe latest update was:\r\n\r\n{{ resolution }}\r\n\r\n",
        },
        "reopened_submitter": {
            "heading": "Ticket Reopened",
            "subject": "(Reopened)",
            "locale": "en",
            "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Your ticket with a subject of <i>{{ ticket.title }}</i> has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">If you wish to view this ticket online, you can visit <a href=\"{{ ticket.ticket_url|safe }}\">{{ ticket.ticket_url|safe }}</a>.</p>",
            "plain_text": "Hello,\r\n\r\nYour ticket with a subject of \"{{ ticket.title }}\" has been reopened.\r\n\r\nIf you wish to view this ticket online, you can visit {{ ticket.ticket_url|safe }}.\r\n\r\n",
        },
    }

    for template_name, defaults in templates.items():
        EmailTemplate.objects.get_or_create(template_name=template_name, locale="en", defaults=defaults)


def remove_reopened_email_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    EmailTemplate.objects.filter(
        template_name__in=["reopened_cc", "reopened_owner", "reopened_submitter"],
        locale="en",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("helpdesk", "0043_fix_on_delete_behaviour"),
    ]

    operations = [
        migrations.RunPython(add_reopened_email_templates, remove_reopened_email_templates),
    ]
