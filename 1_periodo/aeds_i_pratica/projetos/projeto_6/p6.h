#ifndef P6_H
#define P6_H

#define TAM 128

typedef int TMatriz[TAM][TAM];

void imprimirmatriz(TMatriz m,int nl,int nc);
int criamatriz(TMatriz m,int nl,int nc);
void transposta(TMatriz m,int nl,int nc);
void soma(TMatriz m,TMatriz n,int nl,int nc);
void multiplica(TMatriz m,TMatriz n,int la,int ca,int lb,int cb);
void media(TMatriz m,int nl,int nc);

#endif 