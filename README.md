# TP1
Slither.io


8 DE ABRIL

Estuve crenado el escenario y el menu, tambien implemente los puntos en el mapa
con una clase "punto".

Tuve problemas con el primer sistema de menu que pense, asi que lo cambie por una
variable "running menu" que hasta el momento me estaba sirviendo muy bien.

Despues agregue unos botones basicos para probar que funcione, que hasta el momento serian:

- local
- red
- salir

9 DE ABRIL

Comence a implemtenar el gusano, para hacerlo, cree la clase general Serpiente, de la cual
heredarian serpientes con distintos comportamientos, para hacer los bots.
Cree las funciones que tendrian todas las serpientes (bots y jugador):

- crecer
- actualizar
- dibujar
- cambiar direccion
- obtener coliciones

Ademas añadi que la serpiente pueda comer puntos y crecer

10 DE ABRIL (viernes en mi casa)

Le añadi un sprint a la serpiente, al apretar shift cambias un parametro de la clase Serpiente:
self.sprint -> que aumenta la velocidad

El problema que tuve con esto, es que el sistema que tenia para dibujar las serpientes, con
segmentos, que son circulos, funcionaba raro con el sprint, porque al aumentar la velocidad,
la serpiente dibujaba un circulo mas lejos, y se "estiraba", era como si comieses puntos pero
sprinteabas. Para solucionarlo, implemente una variable "largo objetivo", asi ya no dependia tanto
de la posicion, y tenia cuenta el sprint.
Por ultimo añadi al sprint que perdiera tamaño y puntos, para esto, llamaba a la funcion de crecimiento, pero pasandole numeros negativos.

11 DE ABRIL (sabado en mi casa)

Estuve intentando de cambiar el fondo ya que el que tenia en la escuela no me gustaba, pero tuve
muchos problemas, ya que queria usar imagenes de la IA, pero necesitaba que fueran tileables, asi
empieza igual que termina, para poder hacer el mapa abierto. Finalmente cree uno yo pero no me gusto asi que seguro en algun momento lo cambie.

15 DE ABRIl

---