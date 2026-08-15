from django.db import migrations

def cargar_etiquetas_iniciales(apps, schema_editor):
    Categoria = apps.get_model('libros', 'Categoria')
    Estado = apps.get_model('libros', 'Estado')

    categorias = ['Historia', 'Ciencia', 'Infantil', 'General']
    estados = ['En existencia', 'Prestado', 'Perdido', 'En proceso de compra']

    for cat in categorias:
        Categoria.objects.create(titulo=cat)

    for est in estados:
        Estado.objects.create(titulo=est)

def eliminar_etiquetas_iniciales(apps, schema_editor):
    Categoria = apps.get_model('libros', 'Categoria')
    Estado = apps.get_model('libros', 'Estado')
    
    Categoria.objects.filter(titulo__in=['Historia', 'Ciencia', 'Infantil', 'General']).delete()
    Estado.objects.filter(titulo__in=['En existencia', 'Prestado', 'Perdido', 'En proceso de compra']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_etiquetas_iniciales, eliminar_etiquetas_iniciales),
    ]