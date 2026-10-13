from django.db import migrations


TEMPLATES = [
    (161, "reopened_cc", "en", "(Reopened)", "Ticket Reopened"),
    (162, "reopened_owner", "en", "(Reopened)", "Ticket Reopened"),
    (163, "reopened_submitter", "en", "(Reopened)", "Your Ticket Has Been Reopened"),
    (164, "reopened_cc", "cs", "(Reopened)", "Ticket Reopened"),
    (165, "reopened_owner", "cs", "(Reopened)", "Ticket Reopened"),
    (166, "reopened_submitter", "cs", "(Reopened)", "Your Ticket Has Been Reopened"),
    (167, "reopened_cc", "de", "(Reopened)", "Ticket Reopened"),
    (168, "reopened_owner", "de", "(Reopened)", "Ticket Reopened"),
    (169, "reopened_submitter", "de", "(Reopened)", "Your Ticket Has Been Reopened"),
    (170, "reopened_cc", "es", "(Reopened)", "Ticket Reopened"),
    (171, "reopened_owner", "es", "(Reopened)", "Ticket Reopened"),
    (172, "reopened_submitter", "es", "(Reopened)", "Your Ticket Has Been Reopened"),
    (173, "reopened_cc", "fi", "(Reopened)", "Ticket Reopened"),
    (174, "reopened_owner", "fi", "(Reopened)", "Ticket Reopened"),
    (175, "reopened_submitter", "fi", "(Reopened)", "Your Ticket Has Been Reopened"),
    (176, "reopened_cc", "fr", "(Reopened)", "Ticket Reopened"),
    (177, "reopened_owner", "fr", "(Reopened)", "Ticket Reopened"),
    (178, "reopened_submitter", "fr", "(Reopened)", "Your Ticket Has Been Reopened"),
    (179, "reopened_cc", "it", "(Reopened)", "Ticket Reopened"),
    (180, "reopened_owner", "it", "(Reopened)", "Ticket Reopened"),
    (181, "reopened_submitter", "it", "(Reopened)", "Your Ticket Has Been Reopened"),
    (182, "reopened_cc", "pl", "(Reopened)", "Ticket Reopened"),
    (183, "reopened_owner", "pl", "(Reopened)", "Ticket Reopened"),
    (184, "reopened_submitter", "pl", "(Reopened)", "Your Ticket Has Been Reopened"),
    (185, "reopened_cc", "ru", "(Reopened)", "Ticket Reopened"),
    (186, "reopened_owner", "ru", "(Reopened)", "Ticket Reopened"),
    (187, "reopened_submitter", "ru", "(Reopened)", "Your Ticket Has Been Reopened"),
    (188, "reopened_cc", "zh", "(Reopened)", "Ticket Reopened"),
    (189, "reopened_owner", "zh", "(Reopened)", "Ticket Reopened"),
    (190, "reopened_submitter", "zh", "(Reopened)", "Your Ticket Has Been Reopened"),
]


def add_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")

    for pk, template_name, locale, subject, heading in TEMPLATES:
        source = EmailTemplate.objects.get(template_name=template_name.replace("reopened_", "updated_"), locale=locale)
        EmailTemplate.objects.update_or_create(
            pk=pk,
            defaults={
                "template_name": template_name,
                "locale": locale,
                "subject": subject,
                "heading": heading,
                "plain_text": source.plain_text,
                "html": source.html,
            },
        )


def remove_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    EmailTemplate.objects.filter(template_name__startswith="reopened_").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("helpdesk", "0043_fix_on_delete_behaviour"),
    ]

    operations = [
        migrations.RunPython(add_templates, reverse_code=remove_templates),
    ]
