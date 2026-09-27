#include <stdio.h>

float transformacao(float x,float x1,float x2,float y1,float y2){
    float a = (y2 - y1)/(x2 - x1);
    float b = y1 - a*x1;
    return a*x + b;
}

int main(int argc, char const *argv[])
{
    printf("Tranformação Linear para alterar escala de níveis de cinza perante 2 pontos.\n");
    printf("Digite os pontos (x1, y1) e (x2, y2) para a transformação linear:\n");
    float x =0, x1, y1, x2, y2;
    printf("x1: ");
    scanf("%f", &x1);
    printf("y1: ");
    scanf("%f", &y1);
    printf("x2: ");
    scanf("%f", &x2);
    printf("y2: ");
    scanf("%f", &y2);

    for(float i = x1; i <= y1;i++){
        printf("Transformação para x = %f: %f\n", i, transformacao(i,x1, y1, x2, y2));
    }
    for(float i = y1+1; i <= 255;i++){
        printf("Transformação para x = %f: %f\n", i, i);
    }
    
    return 0;
}
