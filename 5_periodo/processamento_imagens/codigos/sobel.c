


int sobel(int in[5][5],int out[5][5]){

    for(int i = 0;i < 5; i ++){
        for(int j = 0; j < 5; j++){
            // Basicamete retiro as bordas aqui  
            if(i == 0 || i == 4 || j == 0 || j == 4){
                out[i][j] = in[i][j];
            }else{
                // Creio que isso pode ser feito em algum for 
                int z0 = in[i-1][j-1];
                int z1 = in[i-1][j];
                int z2 = in[i-1][j+1];
                int z3 = in[i][j-1];
                int z4 = in[i][j];
                int z5 = in[i][j+1];
                int z6 = in[i+1][j-1];
                int z7 = in[i+1][j];
                int z8 = in[i+1][j+1];

                // formula de sobel
                out [i][j] = abs((z2 + 2*z5 + z8) - (z0 + 2*z3 + z6)) + abs((z0 + 2*z1 + z2) - (z6 + 2*z7 + z8));
            }
        }
    }
} 