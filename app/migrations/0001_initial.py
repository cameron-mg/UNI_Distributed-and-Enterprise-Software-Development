# Generated by Django 4.1.6 on 2023-04-03 01:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('CUSTOMER', 'Customer'), ('CLUBREP', 'Club Representative'), ('ACCOUNTMAN', 'Account Manager'), ('CINEMAMAN', 'Cinema Manager')], max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('number', models.CharField(max_length=4)),
                ('street', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('postCode', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('clubid', models.CharField(max_length=8, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('discount', models.IntegerField()),
                ('balance', models.FloatField()),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.address')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('landline', models.CharField(max_length=12)),
                ('mobile', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=20)),
                ('surName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('initial', models.CharField(max_length=1)),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('ageRatings', models.CharField(choices=[('U', 'U'), ('PG', 'PG'), ('12', '12'), ('12A', '12A'), ('15', '15'), ('18', '18')], default='12', max_length=3)),
                ('duration', models.IntegerField()),
                ('desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('cardNumber', models.CharField(max_length=19, unique=True)),
                ('expiryDate', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('screenNo', models.IntegerField()),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField()),
                ('cost', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
                ('madeby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Showing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('remainingSeats', models.IntegerField()),
                ('price', models.FloatField()),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.film')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.screen')),
            ],
        ),
        migrations.CreateModel(
            name='ClubRep',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.contact')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.contact'),
        ),
        migrations.AddField(
            model_name='club',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.payment'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('tickettype', models.CharField(max_length=10)),
                ('cost', models.FloatField()),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.payment')),
                ('showing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.showing')),
            ],
        ),
        migrations.CreateModel(
            name='BlockBooking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField()),
                ('cost', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.club')),
            ],
        ),
    ]
