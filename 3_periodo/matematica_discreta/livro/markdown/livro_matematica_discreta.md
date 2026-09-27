# Matemática Discreta - Livro de Revisão

# Fundamentos de lógica proposicional

## Proposições e valor lógico

Uma proposição é uma sentença declarativa à qual se pode atribuir exatamente um valor lógico: verdadeiro ou falso. Perguntas, ordens e expressões abertas não são proposições. A frase “7 é primo” é uma proposição verdadeira; “feche a porta” não possui valor lógico; e “x é par” só se torna proposição depois que o valor de x é fixado ou quantificado.

Essa distinção parece simples, mas evita um erro recorrente: tentar aplicar conectivos lógicos a frases cujo significado ainda depende de contexto. Ao formalizar um argumento, o primeiro passo é definir proposições atômicas claras. Por exemplo, p pode representar “o programa termina” e q pode representar “a entrada é válida”.

## Conectivos

Os principais conectivos são negação, conjunção, disjunção, implicação e bicondicional. A negação de p, escrita $\neg p$, inverte seu valor lógico. A conjunção $p\land q$ é verdadeira somente quando ambas as parcelas são verdadeiras. A disjunção inclusiva $p\lor q$ é falsa somente quando ambas são falsas.

A implicação $p\to q$ é falsa apenas quando p é verdadeira e q é falsa. Isso reflete o compromisso expresso pela frase “se p, então q”: a única violação ocorre quando a condição se realiza, mas a consequência prometida não. A bicondicional $p\leftrightarrow q$ é verdadeira quando p e q têm o mesmo valor lógico.

> **Exemplo.** Se p significa “n é múltiplo de 4” e q significa “n é par”, então $p\to q$ é verdadeira para todo inteiro n. A recíproca $q\to p$ é falsa: 6 é par, mas não é múltiplo de 4.

## Equivalências úteis

Duas fórmulas são logicamente equivalentes quando possuem a mesma coluna final em todas as linhas da tabela-verdade. Algumas equivalências aparecem continuamente em provas e simplificações:

- dupla negação: $\neg(\neg p)\equiv p$;
- implicação: $p\to q\equiv\neg p\lor q$;
- contrapositiva: $p\to q\equiv\neg q\to\neg p$;
- leis de De Morgan: $\neg(p\land q)\equiv\neg p\lor\neg q$ e $\neg(p\lor q)\equiv\neg p\land\neg q$;
- bicondicional: $p\leftrightarrow q\equiv(p\to q)\land(q\to p)$.

As leis de De Morgan mostram que, ao negar uma expressão composta, o conectivo muda e cada componente é negado. Em programação, isso ajuda a revisar condições complexas e a evitar inversões incorretas.

## Quantificadores e negação

O quantificador universal $\forall$ afirma que uma propriedade vale para todos os elementos do domínio. O quantificador existencial $\exists$ afirma que existe pelo menos um elemento para o qual a propriedade vale. A ordem dos quantificadores importa: $\forall x\,\exists y\,P(x,y)$ não significa o mesmo que $\exists y\,\forall x\,P(x,y)$.

Negar um quantificador troca seu tipo e nega a propriedade:

$$\neg(\forall x\,P(x))\equiv\exists x\,\neg P(x),$$

$$\neg(\exists x\,P(x))\equiv\forall x\,\neg P(x).$$

> **Exemplo.** A negação de “todo arquivo possui backup” é “existe pelo menos um arquivo que não possui backup”. Não é correto dizer “nenhum arquivo possui backup”.

## Exercícios de fixação

- Classifique como proposição ou não: “3 é ímpar”, “qual é sua idade?” e “x+1=5”.
- Escreva a contrapositiva de “se um grafo é uma árvore, então ele é conexo”.
- Negue: “para todo usuário existe uma senha válida”.
- Verifique por tabela-verdade que $p\to q$ equivale a $\neg q\to\neg p$.

# Linguagem matemática e técnicas de demonstração

## Axiomas, conjecturas e teoremas

Um axioma é aceito como ponto de partida dentro de uma teoria. Uma conjectura é uma afirmação apoiada por evidências, mas ainda sem demonstração. Um teorema é uma afirmação demonstrada a partir de definições, axiomas e resultados anteriores. Um lema é um resultado auxiliar usado na prova de outro resultado; um corolário decorre de modo quase imediato de um teorema.

Uma demonstração não é apenas uma sequência de contas. Ela deve declarar hipóteses, indicar o objetivo e justificar cada passagem. Exemplos numéricos podem sugerir um resultado, mas não provam uma afirmação universal.

## Prova direta

Para provar uma implicação $p\to q$ diretamente, assume-se p e, usando definições e resultados conhecidos, deduz-se q.

> **Exemplo.** Provar que a soma de dois inteiros pares é par. Se $m=2a$ e $n=2b$, com a e b inteiros, então $m+n=2a+2b=2(a+b)$. Como $a+b$ é inteiro, $m+n$ é par.

Um cuidado importante é não reutilizar a mesma variável para representar testemunhas independentes. Escrever $m=2k$ e $n=2k$ força indevidamente $m=n$. O correto é usar, por exemplo, $m=2a$ e $n=2b$.

## Contrapositiva e contradição

Como $p\to q$ equivale a $\neg q\to\neg p$, às vezes é mais fácil provar a contrapositiva. Para mostrar “se $n^2$ é par, então n é par”, pode-se provar que, se n é ímpar, então $n^2$ também é ímpar.

Na prova por contradição, assume-se a negação do objetivo e mostra-se que essa hipótese leva a uma impossibilidade. A contradição deve surgir de modo explícito: uma afirmação e sua negação, uma violação de hipótese ou um resultado incompatível com uma propriedade conhecida.

## Como revisar uma prova

- As variáveis e seus domínios foram declarados?
- Cada hipótese foi usada de forma legítima?
- O argumento prova a afirmação, ou apenas a repete com outras palavras?
- Um caso particular foi confundido com uma prova geral?
- A conclusão obtida é exatamente a conclusão pedida?

> **Erro clássico.** Começar uma prova de “se p, então q” assumindo q. Isso pode produzir raciocínio circular. Em uma prova direta, assume-se p; q deve ser deduzida.

# Conjuntos e operações

## Elementos, subconjuntos e conjunto das partes

Escrevemos $x\in A$ quando x é elemento de A e $A\subseteq B$ quando todo elemento de A também pertence a B. As afirmações $x\in A$ e $\{x\}\subseteq A$ são relacionadas, mas não idênticas: a primeira compara elemento e conjunto; a segunda compara dois conjuntos.

O conjunto vazio $\varnothing$ não possui elementos. Já $\{\varnothing\}$ possui um elemento: o próprio conjunto vazio. Para um conjunto finito com n elementos, seu conjunto das partes $\mathcal{P}(A)$ possui $2^n$ subconjuntos.

## União, interseção e diferença

A união $A\cup B$ reúne os elementos que pertencem a A ou a B. A interseção $A\cap B$ contém os elementos comuns. A diferença $A\setminus B$ contém os elementos de A que não pertencem a B. Dado um universo U, o complemento de A é $A^c=U\setminus A$.

As leis de De Morgan para conjuntos são:

$$ (A\cup B)^c=A^c\cap B^c, \qquad (A\cap B)^c=A^c\cup B^c. $$

Elas podem ser provadas pelo método de dupla inclusão: demonstra-se primeiro que o conjunto da esquerda está contido no da direita e depois a inclusão contrária.

## Produto cartesiano

O produto cartesiano $A\times B$ é o conjunto de pares ordenados $(a,b)$ com $a\in A$ e $b\in B$. A ordem importa: em geral, $A\times B\neq B\times A$. Se A e B são finitos, então $|A\times B|=|A|\,|B|$.

> **Exemplo.** Se $A=\{1,2\}$ e $B=\{x,y,z\}$, então $A\times B$ possui seis pares. O par $(1,x)$ não é igual a $(x,1)$.

## Estratégia para identidades de conjuntos

Para provar $A\times(B\cap C)=(A\times B)\cap(A\times C)$, escolha um par arbitrário $(x,y)$ no lado esquerdo. Então $x\in A$ e $y\in B\cap C$, logo y pertence a B e a C. Assim, $(x,y)$ pertence simultaneamente a $A\times B$ e a $A\times C$. A inclusão oposta segue revertendo os passos.

# Indução matemática

## Estrutura da prova

O princípio da indução finita é usado para provar uma propriedade $P(n)$ para todos os inteiros a partir de um valor inicial. A prova tem duas partes inseparáveis:

- base: verificar $P(n_0)$;
- passo indutivo: assumir $P(k)$ para um k arbitrário e provar $P(k+1)$.

A hipótese de indução não afirma que a propriedade é verdadeira para todos os números; ela permite usar $P(k)$ temporariamente para construir o próximo caso.

## Soma dos números ímpares

Vamos provar que $1+3+\cdots+(2n-1)=n^2$. Para $n=1$, ambos os lados valem 1. Suponha agora que a soma dos k primeiros ímpares seja $k^2$. Ao acrescentar o próximo ímpar, obtemos

$$k^2+[2(k+1)-1]=k^2+2k+1=(k+1)^2.$$

Portanto, a fórmula vale para todo $n\geq1$.

## Divisibilidade

Para provar que $n^3-n$ é divisível por 3, há uma demonstração algébrica curta:

$$n^3-n=n(n-1)(n+1).$$

Esse é o produto de três inteiros consecutivos, e um deles é múltiplo de 3. A observação também ajuda a construir uma prova por indução: a diferença entre os casos consecutivos é

$$[(k+1)^3-(k+1)]-(k^3-k)=3k(k+1),$$

que é múltipla de 3.

## Sequências recorrentes

Se $a_1=3$ e $a_k=7a_{k-1}$ para $k\geq2$, a forma fechada é $a_n=3\cdot7^{n-1}$. A base é imediata. No passo, se $a_k=3\cdot7^{k-1}$, então

$$a_{k+1}=7a_k=7\cdot3\cdot7^{k-1}=3\cdot7^k.$$

## Diagnóstico de uma indução incompleta

- Sem a base, a cadeia lógica pode começar em lugar nenhum.
- Sem usar a hipótese de indução, o argumento normalmente é uma prova direta disfarçada ou possui uma lacuna.
- O passo deve provar o caso $k+1$, não repetir o caso k.
- Se a recorrência depende de dois termos anteriores, pode ser necessário assumir dois casos ou usar indução forte.

# Relações binárias

## Definição e representação

Uma relação de A em B é qualquer subconjunto de $A\times B$. Quando A=B, dizemos que a relação é “em A”. Relações finitas podem ser representadas por pares ordenados, diagramas de setas, matrizes ou grafos dirigidos.

Uma relação R em A é reflexiva quando $xRx$ para todo x; simétrica quando $xRy$ implica $yRx$; antissimétrica quando $xRy$ e $yRx$ implicam x=y; e transitiva quando $xRy$ e $yRz$ implicam $xRz$.

## Relações de equivalência

Uma relação de equivalência é reflexiva, simétrica e transitiva. Ela particiona o conjunto em classes de equivalência. Congruência módulo m é o exemplo central:

$$a\equiv b\pmod m \quad\Longleftrightarrow\quad m\mid(a-b).$$

Os inteiros que deixam o mesmo resto na divisão por m pertencem à mesma classe.

## Ordens parciais

Uma ordem parcial é reflexiva, antissimétrica e transitiva. Nem todos os pares precisam ser comparáveis. A relação de inclusão $\subseteq$ no conjunto das partes é uma ordem parcial. Já $\leq$ nos reais é uma ordem total, pois quaisquer dois reais podem ser comparados.

> **Armadilha.** Simetria e antissimetria não são opostos. Uma relação pode ser simultaneamente simétrica e antissimétrica, como a igualdade.

## Fechos

O fecho reflexivo adiciona todos os pares $(x,x)$ ausentes. O fecho simétrico adiciona $(y,x)$ sempre que $(x,y)$ aparece. O fecho transitivo adiciona as conexões exigidas por caminhos de comprimento maior que um. Em computação, o fecho transitivo modela alcançabilidade.

# Funções

## Definição

Uma função $f:A\to B$ associa a cada elemento do domínio A exatamente um elemento do contradomínio B. O conjunto imagem é formado pelos valores realmente atingidos. Domínio, contradomínio e regra de associação fazem parte da definição; duas funções com a mesma fórmula podem ser diferentes se seus domínios ou contradomínios diferem.

## Injetividade, sobrejetividade e bijetividade

Uma função é injetiva quando entradas distintas produzem saídas distintas. Equivalentemente, $f(x_1)=f(x_2)$ implica $x_1=x_2$. Ela é sobrejetiva quando todo elemento do contradomínio é imagem de algum elemento do domínio. É bijetiva quando possui as duas propriedades.

> **Exemplo.** A função $f:\mathbb{R}\to\mathbb{R}$, $f(x)=x+2$, é bijetiva. A igualdade $f(x_1)=f(x_2)$ implica $x_1=x_2$, provando injetividade. Para qualquer $y\in\mathbb{R}$, escolher $x=y-2$ produz $f(x)=y$, provando sobrejetividade.

## Composição e inversa

Se $f:A\to B$ e $g:B\to C$, então $(g\circ f)(x)=g(f(x))$. A ordem é essencial: em geral, $g\circ f\neq f\circ g$. Uma função admite inversa funcional se e somente se é bijetiva.

Para encontrar a inversa de $f(x)=ax+b$, com $a\neq0$, escreva $y=ax+b$ e isole x:

$$x=\frac{y-b}{a}.$$

Logo, $f^{-1}(y)=(y-b)/a$, respeitando os domínios apropriados.

## Funções definidas por partes

Ao compor funções definidas por partes, a condição deve ser aplicada ao argumento interno. Se $f(u)$ muda de regra conforme $u\leq3$ ou $u>3$, então em $f(g(x))$ é necessário resolver quando $g(x)\leq3$ e quando $g(x)>3$.

# Princípios de contagem e combinatória

## Princípios aditivo e multiplicativo

Se uma escolha pode ser feita de a maneiras ou, em caso disjunto, de b maneiras, existem $a+b$ possibilidades. Se um processo possui etapas sucessivas independentes com a e b opções, existem $ab$ resultados.

> **Exemplo.** Um teste de 10 questões com cinco alternativas possui $5^{10}$ gabaritos possíveis: para cada uma das dez posições há cinco escolhas.

## Permutações e arranjos

O número de ordenações de n objetos distintos é $n!$. Quando há repetições com multiplicidades $n_1,\ldots,n_k$, o número de sequências distintas é

$$\frac{n!}{n_1!\cdots n_k!}.$$

Escolher e ordenar k elementos distintos dentre n produz o arranjo

$$A(n,k)=\frac{n!}{(n-k)!}.$$

## Combinações

Quando a ordem não importa, usamos

$$\binom{n}{k}=\frac{n!}{k!(n-k)!}.$$

Uma forma segura de decidir entre arranjo e combinação é perguntar se trocar a ordem dos selecionados cria um resultado diferente. Escolher presidente, vice e secretário exige ordem; escolher três representantes para uma cerimônia não.

## Agrupamentos e divisões

Para dividir 12 pessoas em dois grupos não rotulados de 6, escolher o primeiro grupo e depois dividir por 2 corrige a troca dos grupos:

$$\frac{1}{2}\binom{12}{6}.$$

Em grupos rotulados, como “equipe A” e “equipe B”, essa divisão por 2 não é feita.

## Inclusão-exclusão

Para conjuntos finitos,

$$|A\cup B|=|A|+|B|-|A\cap B|.$$

O termo da interseção é subtraído porque foi contado duas vezes. Com três conjuntos, somam-se os tamanhos individuais, subtraem-se as interseções dois a dois e soma-se novamente a interseção tripla.

# Estratégias para resolução de listas

## Traduzir antes de calcular

Em lógica, defina as proposições atômicas antes de manipular símbolos. Em conjuntos, determine o universo e o significado de cada operação. Em funções, registre domínio e contradomínio. Em combinatória, identifique se a ordem importa, se há repetição e se os grupos são rotulados.

## Testar casos pequenos

Casos pequenos não substituem uma prova, mas ajudam a detectar fórmulas incorretas. Para uma afirmação sobre subconjuntos, teste conjuntos com zero, um e dois elementos. Para recorrências, calcule os primeiros termos. Para identidades combinatórias, compare os dois lados para valores pequenos de n.

## Trabalhar de trás para frente

Quando o objetivo é uma igualdade, examine a forma final desejada e identifique qual transformação intermediária a produziria. Em indução, escreva o caso $k+1$ e tente separar uma parcela correspondente ao caso k. Em provas de conjuntos, traduza o pertencimento ao conjunto final em condições lógicas.

## Verificação dimensional e de domínio

Uma resposta combinatória deve ser inteira e não negativa. Uma inversa precisa respeitar domínio e imagem. Uma expressão como $\binom{n}{k}$ exige $0\leq k\leq n$. A checagem de domínio elimina muitos erros antes mesmo da revisão algébrica.

# Revisão integrada

## Problema 1 - negação com quantificadores

Negue a afirmação: “para todo inteiro n existe um inteiro m maior que n e primo”. A estrutura é $\forall n\,\exists m\,P(n,m)$. A negação correta é $\exists n\,\forall m\,\neg P(n,m)$: “existe um inteiro n tal que nenhum inteiro m maior que n é primo”. A afirmação negada é falsa, mas sua forma lógica está correta.

## Problema 2 - bijeção

Considere $f:\mathbb{Z}\to\mathbb{Z}$, $f(n)=n+2$. Ela é injetiva porque $n_1+2=n_2+2$ implica $n_1=n_2$. É sobrejetiva porque, dado $y\in\mathbb{Z}$, o inteiro $n=y-2$ satisfaz $f(n)=y$. Logo, f é bijetiva e $f^{-1}(y)=y-2$.

## Problema 3 - indução

Prove que $1+2+\cdots+n=n(n+1)/2$. A base $n=1$ é imediata. Supondo a fórmula para k,

$$1+\cdots+k+(k+1)=\frac{k(k+1)}{2}+(k+1)=\frac{(k+1)(k+2)}{2},$$

que é a fórmula para $k+1$.

## Problema 4 - contagem

Quantas palavras de cinco letras distintas podem ser formadas com um alfabeto de 26 letras, contendo A mas sem A na primeira posição? Escolha a posição de A entre as quatro posições permitidas e preencha as demais com quatro letras distintas escolhidas e ordenadas entre as 25 restantes:

$$4\cdot A(25,4)=4\cdot25\cdot24\cdot23\cdot22.$$

## Checklist para provas e avaliações

- Declare o domínio das variáveis.
- Separe hipótese e conclusão.
- Cite a definição usada em cada argumento central.
- Em indução, identifique base, hipótese e passo.
- Em relações, teste cada propriedade separadamente.
- Em funções, não confunda contradomínio com imagem.
- Em contagem, decida primeiro se a ordem e a repetição importam.
- Revise se o resultado responde exatamente ao que foi perguntado.

# Apêndice - fórmulas essenciais

## Lógica e conjuntos

$$p\to q\equiv\neg p\lor q, \qquad p\to q\equiv\neg q\to\neg p.$$

$$\neg(\forall x\,P(x))\equiv\exists x\,\neg P(x), \qquad \neg(\exists x\,P(x))\equiv\forall x\,\neg P(x).$$

$$|A\cup B|=|A|+|B|-|A\cap B|.$$

## Contagem

$$P_n=n!, \qquad A(n,k)=\frac{n!}{(n-k)!}, \qquad \binom{n}{k}=\frac{n!}{k!(n-k)!}.$$

## Fontes internas utilizadas

Este livro foi escrito como material autoral de revisão a partir das Listas 1 a 10 de Matemática Discreta de 2025/1 e das anotações digitalizadas presentes em `resumos/originais/`. As transcrições automáticas foram usadas apenas como apoio de localização; trechos incertos não foram reproduzidos como fatos.

