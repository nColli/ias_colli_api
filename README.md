# ias_colli_api
Trabajo práctico para "Implementación y Actualización de Software" UM


Para ejecutar app: 
```bash
gunicorn wsgi:app
```

Crear y publicar branch:
(Por convención los nombres de cada branch utilizan el prefijo feature/nombre-feature)
```bash
git checkout develop

git pull

git branch feature/<feature-name>

git checkout <branch-name>

git push -u origin <branch-name>
```

### Fuentes
Información sobre crear una base de datos Postgresql en un container para el CI:\
[Documentación Github create-postgresql-service-containers](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers)\
[Documentación Github Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
