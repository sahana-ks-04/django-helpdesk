from django.db import migrations


def forwards_func(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    db_alias = schema_editor.connection.alias

    updated_templates = EmailTemplate.objects.using(db_alias).filter(
        template_name__in=["updated_cc", "updated_owner", "updated_submitter"]
    )

    for updated_template in updated_templates:
        reopened_template_name = updated_template.template_name.replace(
            "updated_", "reopened_"
        )
        if EmailTemplate.objects.using(db_alias).filter(
            template_name=reopened_template_name,
            locale=updated_template.locale,
        ).exists():
            continue

        EmailTemplate.objects.using(db_alias).create(
            template_name=reopened_template_name,
            subject="(Reopened)",
            heading="Ticket Reopened",
            plain_text=updated_template.plain_text,
            html=updated_template.html,
            locale=updated_template.locale,
        )


def reverse_func(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    db_alias = schema_editor.connection.alias
    EmailTemplate.objects.using(db_alias).filter(
        template_name__in=["reopened_cc", "reopened_owner", "reopened_submitter"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("helpdesk", "0043_fix_on_delete_behaviour"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
