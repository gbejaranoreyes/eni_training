from django.test import TestCase
from .models import Convocatoria
from django.contrib.auth.models import User, Group

# Create your tests here.


class ConvocatoriaTestCase(TestCase):
    def test_crear_convocatoria(self):
        convocatoria = Convocatoria.objects.create(
            titulo = "Curso de Python Avanzado",
            area = "Tecnología",
            descripcion = "Capacitación en desarrollo backend",
            fecha_inicio = "2026-10-01",
            fecha_final = "2026-10-15",
            ciudad = "Bogotá",
            cupos_totales = 30,
        )
        self.assertEqual(convocatoria.titulo, "Curso de Python Avanzado")
        self.assertEqual(convocatoria.cupos_asignados, 0)
        self.assertEqual(convocatoria.estado, "Borrador")


#####################################
# pruebas de integración

class ConvocatoriaIntegracionTestCase(TestCase):
    def setUp(self):
        self.grupo = Group.objects.create(name='Administradores')
        self.usuario_admin = User.objects.create_user(username='admin', password='admin123')
        self.usuario_admin.groups.add(self.grupo)
        self.client.login(username='admin', password='admin123')

    def test_crear_convocatoria_integracion(self):
        respuesta = self.client.get('/convocatorias/crear/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'app_convocatorias/app_convocatorias_form.html')
        datos_convocatoria = {
            'titulo': 'Curso Python Avanzado',
            'area': 'Tecnología',
            'descripcion': 'Capacitación en desarrollo backend',
            'fecha_inicio': '2026-10-01',
            'fecha_final': '2026-10-15',  # Nombre del campo según tu vista
            'ciudad': 'Bogotá',
            'cupos_totales': '30',
        }
        respuesta_post = self.client.post('/convocatorias/crear/', datos_convocatoria)
        self.assertEqual(Convocatoria.objects.count(), 1)
        convocatoria_creada = Convocatoria.objects.first()
        self.assertEqual(convocatoria_creada.titulo, 'Curso Python Avanzado')
        self.assertEqual(convocatoria_creada.area, 'Tecnología')
        self.assertEqual(convocatoria_creada.estado, 'Borrador')
        self.assertEqual(convocatoria_creada.cupos_asignados, 0)
        self.assertEqual(respuesta_post.status_code, 302)
        self.assertRedirects(respuesta_post, '/convocatorias/')
        respuesta_convocatorias = self.client.get('/convocatorias/')
        self.assertContains(respuesta_convocatorias, 'Curso Python Avanzado')
        

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Convocatoria


class ConvocatoriaTestCase(TestCase):

    def test_crear_convocatoria(self):
        convocatoria = Convocatoria.objects.create(
            titulo="Curso de Python Avanzado",
            area="Tecnología",
            descripcion="Capacitación en desarrollo backend",
            fecha_inicio="2026-10-01",
            fecha_final="2026-10-15",
            ciudad="Bogotá",
            cupos_totales=30,
        )

        self.assertEqual(convocatoria.titulo, "Curso de Python Avanzado")
        self.assertEqual(convocatoria.cupos_asignados, 0)
        self.assertEqual(convocatoria.estado, "Borrador")

from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Convocatoria


class ConvocatoriaTestCase(TestCase):

    def test_crear_convocatoria(self):
        convocatoria = Convocatoria.objects.create(
            titulo="Curso de Python Avanzado",
            area="Tecnología",
            descripcion="Capacitación en desarrollo backend",
            fecha_inicio="2026-10-01",
            fecha_final="2026-10-15",
            ciudad="Bogotá",
            cupos_totales=30,
        )

        self.assertEqual(convocatoria.titulo, "Curso de Python Avanzado")
        self.assertEqual(convocatoria.cupos_asignados, 0)
        self.assertEqual(convocatoria.estado, "Borrador")


    def test_fecha_final_no_puede_ser_anterior_fecha_inicio(self):

        convocatoria = Convocatoria(
            titulo="Taller Liderazgo",
            area="Administración",
            descripcion="Habilidades blandas",
            fecha_inicio="2026-10-15",
            fecha_final="2026-10-10",
            ciudad="Cali",
            cupos_totales=15,
        )

        with self.assertRaises(ValidationError) as error:
            convocatoria.full_clean()

        self.assertIn(
            "La fecha final no puede ser anterior a la fecha de inicio",
            str(error.exception)
        )

        self.assertEqual(Convocatoria.objects.count(), 0)

        print(
            "PRUEBA EXITOSA: La validación de fechas funciona correctamente."
        )
  