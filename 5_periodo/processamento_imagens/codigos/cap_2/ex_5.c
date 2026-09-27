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

/*
Numa MATRIZ 4x4 ao reduzir pela metade, a nova matriz 2x2 tera os seguintes pixels:
1° passada 0,0 -> r = 0, c = 0   out 0,0 = 0,0 da imagem original
2° passada 0,1 -> r = 0, c = 2   out 0,1 = 0,2 da imagem original 
3° passada 1,0 -> r = 2, c = 0   out 1,0 = 2,0 da imagem original
4° passada 1,1 -> r = 2, c = 2   out 1,1 = 2,2 da imagem original
*/

image img_sampling(image In, float q) {
    if (!In) return NULL;
    
    int total = In->nr * In->nc;
    int jump, new_nr, new_nc;
    if (q == 0.5){
        jump = 2;
        new_nr = In->nr/2;
        new_nc = In->nc/2;

    }else{ // q = 0.25
        jump = 4;
        new_nr = In->nr/4;
        new_nc = In->nc/4;
    }

    image Out = img_create(new_nr, new_nc, In->ml, In->tp);   

    for(int i = 0; i < new_nr; i++) {
        for(int j = 0; j < new_nc;j++){
            int r_actual = i*jump;
            int c_actual = j*jump;
            Out->px[i*new_nc + j] = In->px[r_actual*In->nc + c_actual];
        }
    }

    char filename[50];
    sprintf(filename, "sampled_%2.2f.pgm", q);
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
    
    printf("Redução dos níveis da resolução da imagem pela metade\n");
    img_sampling(img, 0.5);    
    printf("Redução dos níveis da resolução da imagem pela quarta parte\n");
    img_sampling(img, 0.25);    

    img_free(img);
    return 0;
}