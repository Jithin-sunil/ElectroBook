from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.FileField(upload_to='Assets/Seller/product/gallery/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Seller.tbl_product')),
            ],
        ),
    ]

