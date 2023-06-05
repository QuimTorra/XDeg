# XDeg

/εgzdi'ʒi/ [noun]: Xtra Distributed energy

## Port Assigning

- DirectoryAgent: 9000

- AgentePersonal: 9001

> Los agentes internos utilizaran el prefijo 901x

- Organizador: 9010
- GestorTransporte: 9011
- _GestorAlojamiento: 9012_
- _GestorActividades: 9013_
  ...

> Los agentes externos utilizaran el prefijo 905x

- AgenciaTransporte: 9050
- _AgenciaAlojamiento: 9051_
- _AgenciaActividades: 9052_
- _AgenciaTiempo: 9053_

> Los Agentes marcados en cursiva estan pendientes de implementacion y sujetos a cambios

## Usage

To execute the program use the following commands in order:

```
  cd Agentes

  python SimpleDirectoryAgent.py

  python AOrganizador.py
  python AGestorTransporte.py
  *python AGestorAlojamiento.py
  *python AGestorActividades.py

  python AgenciaTransporte.py
  *python AgenciaAlojamiento.py
  *python AgenciaActividades.py
  *python AgenciaTiempo.py

  python PersonalAgent.py
```

![](./OBUNGUS.jpg)
