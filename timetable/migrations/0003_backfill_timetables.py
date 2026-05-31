"""Backfill Timetable rows for existing TimetableSlot records."""
from django.db import migrations


def forwards(apps, schema_editor):
    Timetable = apps.get_model('timetable', 'Timetable')
    TimetableSlot = apps.get_model('timetable', 'TimetableSlot')
    ClassGroup = apps.get_model('academics', 'ClassGroup')

    timetable_map = {}
    for slot in TimetableSlot.objects.order_by('id'):
        if slot.timetable_id:
            continue
        key = (slot.school_id, slot.class_group_id)
        if key not in timetable_map:
            class_group = ClassGroup.objects.filter(pk=slot.class_group_id).first()
            class_name = class_group.name if class_group else 'School'
            name = f'{class_name} timetable'
            counter = 1
            while Timetable.objects.filter(school_id=slot.school_id, name=name).exists():
                counter += 1
                name = f'{class_name} timetable {counter}'
            timetable_map[key] = Timetable.objects.create(
                school_id=slot.school_id,
                name=name,
                class_group_id=slot.class_group_id,
            )
        slot.timetable_id = timetable_map[key].pk
        slot.save(update_fields=['timetable_id'])

    for class_group in ClassGroup.objects.all():
        key = (class_group.school_id, class_group.pk)
        if key in timetable_map:
            continue
        name = f'{class_group.name} timetable'
        counter = 1
        while Timetable.objects.filter(school_id=class_group.school_id, name=name).exists():
            counter += 1
            name = f'{class_group.name} timetable {counter}'
        Timetable.objects.create(
            school_id=class_group.school_id,
            name=name,
            class_group_id=class_group.pk,
        )


def backwards(apps, schema_editor):
    TimetableSlot = apps.get_model('timetable', 'TimetableSlot')
    TimetableSlot.objects.update(timetable_id=None)


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_add_timetable_model'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
