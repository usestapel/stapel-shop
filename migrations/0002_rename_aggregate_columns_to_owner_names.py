# stapel: cutover-phase
#
# ``rating_avg``/``rating_count`` become ``avg``/``count`` — the owner's names,
# which is what makes remote-mode ``read()`` answer the same shape local mode
# already answers (stapel-core's read() contract). Deletion-driven cutover in
# ONE release: the new columns are added, the rows are carried across, and only
# then the old columns die — no release where both names are live.
#
# Safe here for two independent reasons: this fleet deploys stop-the-world (no
# old process writes the drained columns), and the table is a projection
# read-model — derived data with a first-class ``rebuild()`` behind it.
from django.db import migrations, models


def carry_aggregates_forward(apps, schema_editor):
    ListingReviewSummary = apps.get_model("shop", "ListingReviewSummary")
    for row in ListingReviewSummary.objects.all().iterator():
        ListingReviewSummary.objects.filter(pk=row.pk).update(
            avg=row.rating_avg, count=row.rating_count
        )


def carry_aggregates_back(apps, schema_editor):
    ListingReviewSummary = apps.get_model("shop", "ListingReviewSummary")
    for row in ListingReviewSummary.objects.all().iterator():
        ListingReviewSummary.objects.filter(pk=row.pk).update(
            rating_avg=row.avg, rating_count=row.count
        )


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="listingreviewsummary",
            name="avg",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="listingreviewsummary",
            name="count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(carry_aggregates_forward, carry_aggregates_back),
        migrations.RemoveField(
            model_name="listingreviewsummary",
            name="rating_avg",
        ),
        migrations.RemoveField(
            model_name="listingreviewsummary",
            name="rating_count",
        ),
    ]
