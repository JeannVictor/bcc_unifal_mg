#include <stdio.h>
#include <stdlib.h>

typedef struct image
{
    int nr,  // number of rows
        nc,  // number of columns
        ml,  // max gray level
        tp;  // type of image (BW, GRAY, COLOR)
    int *px; // pixels vector (nr * nc)
} *image;

enum
{
    BW = 1,
    GRAY,
    COLOR
};

/*
 * Image allocation and free routines
 *   nr = number of rows
 *   nc = number of columns
 *   ml = max gray level
 *   tp = type of image
 */
image img_create(int nr, int nc, int ml, int tp)
{
    image img = malloc(sizeof (struct image));
    img->px = malloc(nr * nc * sizeof(int));
    img->nr = nr;
    img->nc = nc;
    img->ml = ml;
    img->tp = tp;
    return img;
}

image img_clone(image In)
{
    return img_create(In->nr, In->nc, In->ml, In->tp);
}

int img_free(image Im)
{
    free(Im->px);
    free(Im);
}

/*
 * Read pnm ascii image
 * Params (in):
 *   name = image file name
 *   tp = image type (BW, GRAY or COLOR)
 * Returns:
 *   image structure
 */
void erro(char *msg) { puts(msg); exit(1); }

image img_get(char *name, int tp) {
    char line[200];
    int nr, nc, ml;
    image img;
    FILE *f;
    f = fopen(name, "rt");
    if (!f) erro("ERROR: file open error");
    fgets(line, 200, f); 
    if (line[0] != 'P' || line[1] != (tp + '0'))
        erro("Wrong type image!");
    fgets(line, 200, f); 
    while (line[0] == '#')
        fgets(line, 200, f);
    sscanf(line, "%d %d", &nc, &nr);
    if (tp != BW)
        fscanf(f, "%d", &ml); 
    else
        ml = 1;
    // Image create
    img = img_create(nr, nc, ml, tp);
    for (int i = 0; i < nr * nc; i++) {
        if (tp != COLOR) {
            int k;
            fscanf(f, "%d", &k);
            img->px[i] = k;
        }
        else {
            int r, g, b;
            fscanf(f, "%d %d %d", &r, &g, &b);
            img->px[i] = (r << 16) | (g << 8) | b;
        }
    }
    fclose(f);
    return img;
}

/*
 * Write pnm image
 * Params:
 *   img = image structure
 *   name = image file name
 *   tp = image type (BW, GRAY or COLOR)
 */
void img_put(image img, char *name, int tp)
{
    int count = 0;
    FILE *f = fopen(name, "wt");
    if (!f)
        erro("ERROR: file creation");
    fprintf(f, "P%c\n", tp + '0');
    fputs("# Created by Jeann Victor\n", f);
    fprintf(f, "%d %d\n", img->nc, img->nr);
    if (tp != BW)
        fprintf(f, "%d\n", img->ml);
    for (int i = 0; i < img->nr * img->nc; i++)
    {
        if (tp != COLOR)
        {
            int k = img->px[i];
            fprintf(f, "%3d ", k);
        }
        else
        {
            int r = (img->px[i] >> 16) & (0xFF);
            int g = (img->px[i] >> 8) & (0xFF);
            int b = img->px[i] & (0xFF);
            fprintf(f, "%d %d %d ", r, g, b);
        }
        count++;
        if (count > 50)
        {
            fprintf(f, "\n");
            count = 0;
        }
    }
}

image img_quantization(image In, int q) {
    if (!In) return NULL;
    
    image Out = img_clone(In);
    int total = In->nr * In->nc;
    int divisor;
    
    switch(q) {
        case 128: divisor = 2; break;
        case 64:  divisor = 4; break;
        case 32:  divisor = 8; break;
        case 16:  divisor = 16; break;
        default: 
            printf("Erro: q deve ser 16, 32, 64 ou 128\n");
            img_free(Out);
            return NULL;
    }
    
    for(int i = 0; i < total; i++) {
        Out->px[i] = (In->px[i] / divisor) * divisor;
    }

    char filename[50];
    sprintf(filename, "quantized_%d.pgm", q);
    img_put(Out, filename, GRAY);

    return Out;
}

int main()
{
    image img = img_get("stanford.pgm", GRAY);
    if (!img) {
        printf("Erro ao carregar imagem!\n");
        return 1;
    }
    
    printf("Redução dos níveis de cinza de 256 para 128\n");
    img_quantization(img, 128);        
    printf("Redução dos níveis de cinza de 256 para 64\n");
    img_quantization(img, 64);
    printf("Redução dos níveis de cinza de 256 para 32\n");
    img_quantization(img, 32);
    printf("Redução dos níveis de cinza de 256 para 16\n");
    img_quantization(img, 16);


    img_free(img);
    return 0;
}