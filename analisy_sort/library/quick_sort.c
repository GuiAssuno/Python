#include <stdio.h>
#include <time.h>
#include <stdlib.h>  

void inverte(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

//========================================= Geradores de Numeros ===========================================
void gerador_numeros_aleatorio(int vetor[], int n){
    srand(time(NULL));
    for (int i = 0; i < n; i++) {
        vetor[i] = rand() % 10000;
    }
}

void gerador_numeros_fixo(int vetor[], int n){
   for (int x = 1; x<=n;x++)
    {    
        srand(x);
        vetor[x] = rand() % 9786; 
    }     
}

void gerador_numeros_repetidos(int vetor[], int n){
    int tanto = (len(vetor)*0.15);

    for (int x = 1,y = 0; x<=n;x++,y++)
    {    
        srand(x);
        vetor[x] = (rand()% len(vetor));

        if ((x == tanto) && (y < (n-tanto)))
            x = 0;
        else
            if (y > (n-tanto))
                x=y;
    }          
}

void gerador_numeros_ordenados(int vetor[], int n){
    for (int x = 0,y = 0; x <= n; x++,y++)
    {    
       vetor[x]= x + (y/2);
    }
}

//=============================================== Pivôs ===========================================

int pivot_ultimo(int vetor[], int n){

    return vetor[n];
}

int pivot_primeiro(int vetor[], int esquerda, int direita){

 inverte(&vetor[esquerda], &vetor[direita]);

    return vetor[direita];

}

int pivot_mediana_3(int vetor[], int esquerda, int direita){
    int meio= (esquerda + direita) / 2;
    int a = vetor[esquerda];
    int b = vetor[meio];
    int c = vetor[direita];
    
    int mediana;

    if ((a <= b && b <= c) || (c <= b && b <= a)) {
        mediana = meio;
    } else if ((b <= a && a <= c) || (c <= a && a <= b)) {
        mediana = esquerda;
    } else {
        mediana = direita;
    }

    inverte(&vetor[mediana], &vetor[direita]);

    return vetor[direita];

}

int pivot_meio(int vetor[], int esquerda, int direita){
    inverte(&vetor[((esquerda + direita) / 2)], &vetor[direita]);

    return vetor[direita];

}

int pivot_aleatorio(int vetor[], int esquerda, int direita){

    int r = esquerda + (rand() % (direita - esquerda + 1));
    inverte(&vetor[r], &vetor[direita]);

    return vetor[direita];

}


//=============================================== Lomuto ===============================================
int lomuto_ultimo_elemento(int vetor[], int esquerda, int direita) {
    int pivo = pivot_ultimo(vetor, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int lomuto_primeiro_elemento(int vetor[], int esquerda, int direita) {

    int pivo = pivot_primeiro(vetor,esquerda,direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int lomuto_mediana_treis(int vetor[], int esquerda, int direita) {
    
    int pivo = pivot_mediana_3(vetor, esquerda, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int lomuto_elemento_aleatorio(int vetor[], int esquerda, int direita) {
    
    int pivo = pivot_aleatorio(vetor, esquerda, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int lomuto_mediana(int vetor[], int esquerda, int direita) {

    int pivo = pivot_meio(vetor, esquerda, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

//=============================================== Hoare ===========================================
int hoare_ultimo_elemento(int vetor[], int esquerda, int direita) {
    int pivo = pivot(vetor, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int hoare_primeiro_elemento(int vetor[], int esquerda, int direita) {

    inverte(&vetor[esquerda], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int hoare_mediana_treis(int vetor[], int esquerda, int direita) {
    
    int meio= (esquerda + direita) / 2;
    int a = vetor[esquerda];
    int b = vetor[meio];
    int c = vetor[direita];
    
    int mediana;

    if ((a <= b && b <= c) || (c <= b && b <= a)) {
        mediana = meio;
    } else if ((b <= a && a <= c) || (c <= a && a <= b)) {
        mediana = esquerda;
    } else {
        mediana = direita;
    }

    inverte(&vetor[mediana], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int hoare_elemento_aleatorio(int vetor[], int esquerda, int direita) {
    
    int r = esquerda + (rand() % (direita - esquerda + 1));

    inverte(&vetor[r], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int hoare_mediana(int vetor[], int esquerda, int direita) {

    // 1. ESCOLHA DO PIVÔ:
    // Pega o valor do elemento do meio (evita pior caso em dados ordenados)
    int pivo_valor = vetor[esquerda + (direita - esquerda) / 2];
    
    // 2. PARTIÇÃO (ESQUEMA DE HOARE):
    int i = esquerda - 1;
    int j = direita + 1;

    while (1) {
        // Encontra elemento à esquerda (i) que é >= pivô
        do {
            i++;
        } while (vetor[i] < pivo_valor);

        // Encontra elemento à direita (j) que é <= pivô
        do {
            j--;
        } while (vetor[j] > pivo_valor);

        // Se os ponteiros se cruzarem, a partição está completa
        if (i >= j) {
            break;
        }

        // Troca os elementos encontrados
        inverte(&vetor[i], &vetor[j]);
    }
    return (j);
}

//=============================================== 3 vias ===========================================
int via_ultimo_elemento(int vetor[], int esquerda, int direita) {
    int pivo = pivot(vetor, direita);
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int via_primeiro_elemento(int vetor[], int esquerda, int direita) {

    inverte(&vetor[esquerda], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int via_mediana_treis(int vetor[], int esquerda, int direita) {
    
    int meio= (esquerda + direita) / 2;
    int a = vetor[esquerda];
    int b = vetor[meio];
    int c = vetor[direita];
    
    int mediana;

    if ((a <= b && b <= c) || (c <= b && b <= a)) {
        mediana = meio;
    } else if ((b <= a && a <= c) || (c <= a && a <= b)) {
        mediana = esquerda;
    } else {
        mediana = direita;
    }

    inverte(&vetor[mediana], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int via_elemento_aleatorio(int vetor[], int esquerda, int direita) {
    
    int r = esquerda + (rand() % (direita - esquerda + 1));

    inverte(&vetor[r], &vetor[direita]);

    int pivo = vetor[direita];
    int i = (esquerda - 1);
    
    for (int j = esquerda; j <= direita - 1; j++) {
        if (vetor[j] < pivo) {
            i++;
            inverte(&vetor[i], &vetor[j]);
        }
    }
    inverte(&vetor[i + 1], &vetor[direita]);
    return (i + 1);
}

int via_mediana(int vetor[], int esquerda, int direita) {

    int pivo = vetor[esquerda];

    int lt = esquerda; // lt (less than) -> limite da seção < pivô
    int gt = direita;  // gt (greater than) -> limite da seção > pivô
    int i = esquerda;  // ponteiro de varredura

    // O loop para quando 'i' cruza 'gt'
    while (i <= gt) {
        if (vetor[i] < pivo) {
            // Elemento é MENOR que o pivô
            inverte(&vetor[lt], &vetor[i]);
            lt++;
            i++;
        } else if (vetor[i] > pivo) {
            // Elemento é MAIOR que o pivô
            inverte(&vetor[i], &vetor[gt]);
            gt--;
            // 'i' não é incrementado, pois o elemento que veio de 'gt'
            // ainda não foi verificado
        } else {
            // Elemento é IGUAL ao pivô
            i++;
        }
    }

}

//=============================================== Setup ===========================================

double inicia_quick_sort(int vetor[], int n, int op) {
    
    clock_t start, fim;
    double tempo;


    void (*algoritmo_escolhido)(int[], int, int, int(*));
    int (*metodo_escolhido)(int[],int,int);

//configurando os algoritimos com seus metodos de escolha de pivo
    if ((op > 210)&&(op < 20))
    {//lomuto
        algoritmo_escolhido = &quick_sort_lomuto;

        switch (op)
        {// opções de pivôs
        case 11:
            metodo_escolhido = &lomuto_ultimo_elemento;
            break;
        case 12:
            metodo_escolhido = &lomuto_primeiro_elemento;
            break;
        case 13:
            metodo_escolhido = &lomuto_mediana_treis;
            break;
        case 14:
            metodo_escolhido = &lomuto_elemento_aleatorio;
            break;
        case 15:
            metodo_escolhido = &lomuto_mediana;
            break;
        
        default:
            break;
        }
    }
    else
        if(op > 20 && (op < 30))
        {//hoare
            algoritmo_escolhido = &quick_sort_hoare;
        switch (op)
        {// opções de pivôs
        case 21:
            metodo_escolhido = &pivot_ultimo;
            break;
        case 22:
            metodo_escolhido = &pivot_primeiro;
            break;
        case 23:
            metodo_escolhido = &pivot_mediana_3;
            break;
        case 24:
            metodo_escolhido = &pivot_meio;
            break;
        case 25:
            metodo_escolhido = &pivot_aleatorio;
            break;
        
        default:
            break;
        }        
    }
    else 
        if(op > 30 && (op < 40))
        {//3 vias 
            algoritmo_escolhido = &quick_sort_3way;
        switch (op)
        {// opções de pivôs
        case 31:
            metodo_escolhido = &pivot_ultimo;
            break;
        case 32:
            metodo_escolhido = &pivot_primeiro;
            break;
        case 33:
            metodo_escolhido = &pivot_mediana_3;
            break;
        case 34:
            metodo_escolhido = &pivot_meio;
            break;
        case 35:
            metodo_escolhido = &pivot_aleatorio;
            break;
        
        default:
            break;
        }        
    }


    start = clock();// inicia a contagem de clock de execução
    
    //executa o algoritmo escolhido junto com seu metodo de escolha de pivo selecionado
    algoritmo_escolhido(vetor, 0, n - 1, metodo_escolhido);  
    
    fim = clock();//termina a contagem de clock de orginização

    //converte contage de clocks para clocks por segundo
    tempo = ((double)(fim - start)) / CLOCKS_PER_SEC;
    
    return tempo; //retorna o tempo de execução
}



void quick_sort_lomuto (int vetor[], int esquerda, int direita, int(*metodo)(int[], int, int)) {
    int parte;

    if (esquerda < direita) 
    {
        parte = metodo(vetor, esquerda, direita);
        quick_sort_lomuto(vetor, esquerda, parte - 1, metodo);
        quick_sort_lomuto(vetor, parte + 1, direita, metodo);
        
    }
}

void quick_sort_hoare(int vetor[], int esquerda, int direita, int(*metodo)(int[], int, int)) {
    int parte;

    if (esquerda >= direita) {
        return;
    }
    parte = metodo(vetor, esquerda, direita);
    quick_sort_hoare(vetor, esquerda, parte,metodo);
    quick_sort_hoare(vetor, parte + 1, direita,metodo);
}

void quick_sort_3way(int vetor[], int esquerda, int direita, int(*metodo)(int[], int, int)) {
    int parlt = 0, pargt =0 ;
    if (esquerda >= direita) {
        return;
    }

    
    // 3. CHAMADAS RECURSIVAS:
    // A mágica: a parte do meio (== pivô) não é incluída
    metodo(vetor, esquerda, direita);
    quick_sort_3way(vetor, esquerda, parlt - 1, metodo);
    quick_sort_3way(vetor, pargt + 1, direita, metodo);
}
