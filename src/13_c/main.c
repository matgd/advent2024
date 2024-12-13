#include <stdio.h>
#define INF 999999

int main(int argc, char *argv[]) 
{ 
    FILE *fptr = fopen(argv[1], "r");
    int ax[400], ay[400], bx[400], by[400], px[400], py[400];

    int i = 0;
    do 
    {
        fscanf(fptr, "Button A: X+%d, Y+%d\n", &ax[i], &ay[i]);
        fscanf(fptr, "Button B: X+%d, Y+%d\n", &bx[i], &by[i]);
        fscanf(fptr, "Prize: X=%d, Y=%d\n", &px[i], &py[i]);
        i++;
    } while (!feof(fptr));
    fclose(fptr);
    
    int tokensspent = 0;
    for (int j = 0; j < i; j++)
    {
        int mincost = INF;
        for (int a = 0; a < 100; a++)
        {
            for (int b = 0; b < 100; b++)
            {
                int posx = a * ax[j] + b * bx[j];
                int posy = a * ay[j] + b * by[j];
                if (posx == px[j] && posy == py[j])
                {
                    int cost = a * 3 + b;
                    if (cost < mincost)
                    {
                        mincost = cost;
                    }
                }
            }
        }
        if (mincost < INF)
        {
            tokensspent += mincost;
        }
    }
    printf("Tokens spent: %d\n", tokensspent);
}
