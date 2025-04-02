from django.db import models
from django.contrib.auth.hashers import make_password






class Celda(models.Model):
    id_celda = models.AutoField(primary_key=True)
    numero_celda = models.CharField(max_length=10)
    capacidad_maxima = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'celda'

    def __str__(self):
        return f'{self.numero_celda} - {self.capacidad_maxima}'
    
    def save(self, *args, **kwargs):
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super(Celda, self).save(*args, **kwargs)


class Detenido(models.Model):
    id_detenido = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento_identidad = models.CharField(max_length=20)
    fecha_ingreso = models.DateTimeField(blank=True, null=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    historial = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'detenido'
        ordering = ['id_detenido']
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.historial:
            self.historial = self.historial.upper()
        super(Detenido, self).save(*args, **kwargs)


class Guardiaseguridad(models.Model):
    id_guardia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    turno = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'guardia_seguridad'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.turno:
            self.turno = self.turno.upper()
        super(Guardiaseguridad, self).save(*args, **kwargs)


class Incidente(models.Model):
    id_incidente = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    id_detenido = models.ForeignKey(Detenido, on_delete=models.CASCADE)
    id_guardia = models.ForeignKey(Guardiaseguridad, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'incidente'
    
    def __str__(self):
        return f'{self.id_detenido} - {self.id_guardia}'
    
    def save(self, *args, **kwargs):
        if self.descripcion:
            self.descripcion = self.descripcion.upper()
        super(Incidente, self).save(*args, **kwargs)


class Ocupacioncelda(models.Model):
    id_ocupacion = models.AutoField(primary_key=True)
    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(blank=True, null=True)
    id_celda = models.ForeignKey(Celda, on_delete=models.CASCADE)
    id_detenido = models.ForeignKey(Detenido, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ocupacion_celda'

    def __str__(self):
        return f'{self.fecha_ingreso}'


class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'permiso'

    def __str__(self):
        return {self.nombre}
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Permiso, self).save(*args, **kwargs)


class Personalmedico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'personalmedico'

    def __str__(self):
        return f'{self.nombre} {self.apellido}-({self.especialidad})'
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.especialidad:
            self.especialidad = self.especialidad.upper()
        super(Personalmedico, self).save(*args, **kwargs)


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'rol'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        super(Rol, self).save(*args, **kwargs)


class Rolpermiso(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'rol_permiso'

    def __str__(self):
        return f'{self.id_permiso}'


class Traslado(models.Model):
    id_traslado = models.AutoField(primary_key=True)
    fecha_traslado = models.DateTimeField()
    motivo = models.TextField()
    id_celda_destino = models.ForeignKey(Celda, on_delete=models.CASCADE, related_name='celda_destino')
    id_celda_origen = models.ForeignKey(Celda, on_delete=models.CASCADE, related_name='celda_origen')
    id_detenido = models.ForeignKey(Detenido, on_delete=models.CASCADE)
    id_guardia = models.ForeignKey(Guardiaseguridad, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'traslado'

    def __str__(self):
        return f'{self.fecha_traslado} - {self.motivo}'
    
    def save(self, *args, **kwargs):
        if self.motivo:
            self.motivo = self.motivo.upper()
        super(Traslado, self).save(*args, **kwargs)


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento_identidad = models.CharField(max_length=20)
    correo = models.EmailField(max_length=150)
    password = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.correo:
            self.correo = self.correo.upper()
        
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)


class Visitante(models.Model):
    id_visitante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento_identidad = models.CharField(max_length=20)
    relacion_con_detenido = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'visitante'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper()
        if self.apellido:
            self.apellido = self.apellido.upper()
        if self.relacion_con_detenido:
            self.relacion_con_detenido = self.relacion_con_detenido.upper()
        super(Visitante, self).save(*args, **kwargs)


class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    fecha_visita = models.DateTimeField()
    tipo_visita = models.CharField(max_length=20)
    estado = models.BooleanField(default=False)
    id_detenido = models.ForeignKey(Detenido, on_delete=models.CASCADE)
    id_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'visita'

    def __str__(self):
        return self.tipo_visita
    
    def save(self, *args, **kwargs):
        if self.tipo_visita:
            self.tipo_visita = self.tipo_visita.upper()
        super(Visita, self).save(*args, **kwargs)


class Atencionmedica(models.Model):
    id_atencion = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    id_detenido = models.ForeignKey(Detenido, on_delete=models.CASCADE)
    id_medico = models.ForeignKey(Personalmedico, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'atencion_medica'

    def __str__(self):
        return f'{self.fecha}'
    
    def save(self, *args, **kwargs):
        if self.diagnostico:
            self.diagnostico = self.diagnostico.upper()
        if self.tratamiento:
            self.tratamiento = self.tratamiento.upper()
        super(Atencionmedica, self).save(*args, **kwargs)


class Auditoria(models.Model):
    id_auditoria = models.AutoField(primary_key=True)
    tabla_afectada = models.CharField(max_length=50)
    id_registro_afectado = models.IntegerField()
    accion = models.CharField(max_length=10)
    fecha_hora = models.DateTimeField()
    detalles = models.JSONField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'auditoria'


