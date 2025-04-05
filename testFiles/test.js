// Este es un comentario de una sola línea

/*
Este es un comentario
de múltiples líneas
*/

function sumar(a, b) {
    // Esta función suma dos números y retorna el resultado
    return a + b;
}

/*
Llamamos a la función sumar
con los valores 5 y 3
*/

function hello() {
    console.log("Hello, world! // this is not a comment");
}

function hello2() {
    console.log("Hello, world! /* this is not a comment */");
}

const resultado = sumar(5, 3);

console.log(resultado); // Imprime el resultado en la consola