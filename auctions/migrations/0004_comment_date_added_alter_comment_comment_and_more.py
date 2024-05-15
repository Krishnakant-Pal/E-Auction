# Generated by Django 4.1.7 on 2024-05-13 16:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_rename_winners_listing_winner_listing_winning_bid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="date_added",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comment",
            name="comment",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="comment",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.listing",
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.CharField(
                choices=[
                    ("Elec", "Electronics"),
                    (" ", "Others"),
                    ("B", "Books"),
                    ("T", "Toys"),
                    ("Clo", "Clothing"),
                    ("H&K", "Home & Kitchen"),
                ],
                max_length=5,
                null=True,
            ),
        ),
    ]
