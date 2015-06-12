.. _quickstart:

Quickstart
==========

.. module:: hpsdnclient.api

Ansioso por empezar? Esta página da una buena introducción en cómo empezar
con el cliente de HP SDN. Si no ha instalado ya,
diríjase a la: ref: `Instalación <install>` sección.

Uso de la API
--------------

Uso del Cliente HP SDN para interactuar con el API HP VAN SDN Controller resto es simple.

Primero importamos el módulo Client HP SDN utilizando el nombre corto `` hp`` ::

    >>> Hpsdnclient importación como hp

Entonces, creamos un autenticador XAuthToken ::

    >>> Auth = hp.XAuthToken (server = 10.10.10.10, user = "SDN", password = "skyline")

Esto crea una: class: `XAuthToken` autenticador llamado` `auth`` que se requiere para crear una instancia del: class:` api` objeto ::

    >>> Api = hp.Api (controller = '10 .10.10.10 ', auth = auth)

Ahora, tenemos una: class: `api` objeto llamado` `api``. Este objeto nos permite acceder a la API de controlador SDN HP VAN mediante llamadas a métodos simples.
Por ejemplo ::

    >>> api.get_datapaths ()

Que devolverá una lista de todos datapaths descubiertos por el controlador HP VAN SDN.

La documentación completa de cada uno de los métodos está disponible en el: ref: `Core API REST <core>`,
: Ref: `OpenFlow REST API <of>` y: ref: `Red de Servicios de la API REST <net>` secciones.

Errores and Excepciones
---------------------

Si las cosas van mal, el cliente de HP SDN elevará excepciones para su aplicación de manejar.
Las siguientes excepciones son criados basado en el mensaje de error dan a nosotros por el controlador HP VAN SDN.

R: class: `~ excepción hpsdnclient.error.InvalidJson` se eleva cuando el JSON presentado en una solicitud POST no es válido

R: class: `~ excepción hpsdnclient.error.VersionMismatch` se eleva cuando un Datapath no admite la versión OpenFlow requisito para una función específica

R: class: `~ excepción hpsdnclient.error.IllegalArgument` se genera cuando un argumento ilegal se pasa al controlador de API SDN

R: class: `~ se eleva excepción hpsdnclient.error.OpenflowProtocolError` cuando el algo va mal en la capa de OpenFlow

R: class: `~ excepción hpsdnclient.error.NotFound` se genera cuando no se encuentra el recurso solicitado

Si algo va mal en la conversión entre JSON y Python objetos, un
: Class: `excepción hpsdnclient.error.DatatypeError` se eleva

Todas las excepciones que el Cliente HP SDN plantea explícitamente heredan de
: Class: `hpsdnclient.error.HpsdnclientError`.

En el caso de un error en la capa HTTP que no se puede manejar, permitimos que la biblioteca Solicitudes para elevar una excepción.
