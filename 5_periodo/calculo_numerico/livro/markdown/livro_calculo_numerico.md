# Cálculo Numérico - Fundamentos, Métodos e Investigações em Python

# Pensamento numérico e qualidade da solução

## Do problema real ao resultado computacional

Cálculo Numérico estuda como obter aproximações confiáveis para problemas matemáticos que não admitem uma solução fechada conveniente, que envolvem dados medidos ou cuja dimensão torna inviável uma solução simbólica. O objetivo não é apenas produzir um número. É construir um processo no qual modelo, algoritmo, implementação e interpretação possam ser auditados.

Um fluxo numérico completo possui quatro camadas. A primeira é a modelagem: quais variáveis, hipóteses e equações representam o fenômeno? A segunda é a discretização ou reformulação: como transformar o problema contínuo ou implícito em operações executáveis? A terceira é o algoritmo: quais propriedades de convergência, estabilidade e custo ele possui? A quarta é a validação: como distinguir uma solução plausível de uma resposta apenas numericamente produzida?

> **Princípio central.** Uma aproximação só é útil quando vem acompanhada de um critério de erro, de um teste de consistência e de informação suficiente para que o experimento seja repetido.

## Erro, resíduo e condicionamento

Se $x^*$ é a solução exata e $\widehat{x}$ é a aproximação, o erro absoluto é $|x^*-\widehat{x}|$. Quando a escala do problema importa, utiliza-se o erro relativo

$$e_r=\frac{|x^*-\widehat{x}|}{|x^*|},$$

desde que $x^*\neq0$. Em muitos problemas a solução exata é desconhecida. Nesse caso, mede-se uma condição que deveria ser satisfeita. Para um sistema $Ax=b$, por exemplo, o resíduo é

$$r=b-A\widehat{x}.$$

Um resíduo pequeno mostra que a aproximação quase satisfaz as equações, mas não garante sozinho que $\widehat{x}$ esteja perto de $x^*$. Se o problema for mal-condicionado, pequenas perturbações em $A$ ou $b$ podem provocar grandes mudanças na solução.

O número de condição de uma matriz não singular é

$$\kappa(A)=\|A\|\,\|A^{-1}\|.$$

Valores próximos de 1 indicam baixa sensibilidade. Valores muito grandes indicam que erros de dados e arredondamento podem ser amplificados. Condicionamento é propriedade do problema; estabilidade é propriedade do algoritmo. Um bom método evita acrescentar uma amplificação desnecessária à sensibilidade que já existe.

## Verificação em três níveis

- verificar casos pequenos cuja resposta é conhecida;
- medir resíduos, erros relativos ou conservação de grandezas;
- variar tolerância, passo, malha e precisão para observar se o comportamento acompanha a teoria.

Nos relatórios anexos, essa estratégia aparece repetidamente: compara-se a solução com rotinas de referência, mede-se o resíduo e depois se altera um parâmetro para observar estabilidade, custo ou convergência.

# Representação numérica e propagação de erros

## Aritmética de ponto flutuante

Computadores representam apenas um subconjunto finito dos números reais. Em notação simplificada, um número de ponto flutuante tem sinal, mantissa e expoente. O resultado de uma operação precisa ser arredondado para o número representável mais próximo. Por isso, em geral,

$$\operatorname{fl}(a\circ b)=(a\circ b)(1+\delta),\qquad |\delta|\leq u,$$

onde $u$ é a unidade de arredondamento e $\circ$ representa uma operação elementar.

As identidades algébricas usuais podem perder validade exata. A adição não é plenamente associativa, comparações por igualdade podem falhar e subtrair números quase iguais pode destruir dígitos significativos.

## Cancelamento catastrófico

Considere $a$ e $b$ próximos. Embora ambos possuam vários algarismos corretos, a diferença $a-b$ pode preservar poucos deles. Esse cancelamento aparece em fórmulas de derivação numérica, raízes de equações quadráticas e avaliações polinomiais mal organizadas.

Uma defesa é reformular a expressão. Outra é escolher uma escala adequada e evitar passos excessivamente pequenos. Na diferenciação por diferenças finitas, diminuir $h$ reduz o erro de truncamento até certo ponto; depois, a divisão por $h$ amplifica arredondamentos e o erro volta a crescer.

## Critérios de parada

Um algoritmo iterativo não deve parar apenas porque atingiu um número fixo de iterações. Critérios comuns são

$$|x_{k+1}-x_k|\leq \varepsilon_a+\varepsilon_r|x_{k+1}|$$

e, quando existe uma equação $f(x)=0$,

$$|f(x_{k+1})|\leq \varepsilon_f.$$

É recomendável combinar um teste de variação, um teste de resíduo e um limite máximo de iterações. Assim, o programa diferencia convergência, estagnação e divergência.

> **Checklist de implementação.** Registre tolerância, norma, máximo de iterações, motivo de parada e quantidade de passos. Sem esses dados, duas execuções aparentemente iguais podem representar critérios muito diferentes.

# Equações não lineares

## Isolamento da raiz

Antes de iterar, é preciso entender onde uma raiz pode estar. Se $f$ é contínua em $[a,b]$ e $f(a)f(b)<0$, o teorema do valor intermediário garante pelo menos uma raiz no intervalo. Essa condição sustenta os métodos de encaixamento.

O gráfico ajuda a formular hipóteses, mas não substitui o teste numérico. Um intervalo largo pode conter várias raízes; uma tangência pode não produzir mudança de sinal; uma descontinuidade pode imitar um cruzamento.

## Bisseção e falsa posição

A bisseção escolhe o ponto médio $m=(a+b)/2$ e conserva a metade que mantém a mudança de sinal. Depois de $k$ iterações, o comprimento do intervalo é

$$\frac{b-a}{2^k}.$$

O método é lento, mas previsível e robusto. A falsa posição substitui o ponto médio pela interseção da secante com o eixo:

$$x=\frac{a f(b)-b f(a)}{f(b)-f(a)}.$$

Ela pode avançar mais rapidamente, mas em funções muito assimétricas um extremo pode permanecer praticamente fixo. O histórico dos intervalos revela esse comportamento.

## Iteração de ponto fixo

Reescreve-se $f(x)=0$ como $x=g(x)$ e aplica-se

$$x_{k+1}=g(x_k).$$

A reformulação não é neutra. Perto do ponto fixo $x^*$, a condição $|g'(x^*)|<1$ favorece convergência local; se $|g'(x^*)|>1$, pequenas perturbações tendem a crescer. Duas formas algébricas equivalentes podem gerar processos com comportamentos opostos.

## Newton e secante

O método de Newton lineariza a função em $x_k$:

$$x_{k+1}=x_k-\frac{f(x_k)}{f'(x_k)}.$$

Quando o ponto inicial é adequado e a raiz é simples, a convergência local costuma ser quadrática. A derivada pequena, uma aproximação inicial ruim ou uma função não regular podem causar saltos e divergência.

O método da secante aproxima a derivada com dois pontos:

$$x_{k+1}=x_k-f(x_k)\frac{x_k-x_{k-1}}{f(x_k)-f(x_{k-1})}.$$

Ele dispensa a derivada analítica e frequentemente oferece um equilíbrio interessante entre custo e velocidade.

## Escolha do método

- use bisseção quando houver um intervalo com mudança de sinal e robustez for prioritária;
- use Newton quando a derivada estiver disponível e uma boa aproximação inicial puder ser obtida;
- use secante quando derivar for caro ou inconveniente;
- use ponto fixo somente depois de analisar a função de iteração;
- em aplicações críticas, combine um método rápido com salvaguarda por intervalo.

# Sistemas lineares: métodos diretos

## Eliminação de Gauss e pivoteamento

A eliminação de Gauss transforma $Ax=b$ em um sistema triangular superior $Ux=c$. A retro-substituição resolve então as incógnitas da última equação para a primeira. O custo dominante para uma matriz densa $n\times n$ cresce como $O(n^3)$.

Dividir por um pivô muito pequeno amplifica erros. No pivoteamento parcial, a linha do maior elemento em módulo da coluna ativa é trocada com a linha do pivô. O relatório de métodos diretos mostra experimentalmente que essa troca reduz drasticamente o erro em aritmética de precisão limitada.

> **Teste mínimo.** Depois de resolver o sistema, calcule $\|A\widehat{x}-b\|$. Para comparar sistemas de escalas diferentes, use também um resíduo relativo, por exemplo $\|A\widehat{x}-b\|/(\|A\|\|\widehat{x}\|+\|b\|)$.

## Fatorações LU e PLU

Na fatoração LU, escreve-se

$$A=LU,$$

com $L$ triangular inferior e $U$ triangular superior. Uma vez fatorada a matriz, cada novo vetor $b$ exige apenas duas substituições triangulares. Isso é vantajoso quando a mesma matriz aparece com muitos lados direitos.

Com pivoteamento, a forma apropriada é $PA=LU$, em que $P$ registra as trocas de linha. Ignorar $P$ ao verificar a fatoração é um erro frequente.

## Cholesky

Se $A$ é simétrica definida positiva, existe uma fatoração

$$A=LL^T.$$

Cholesky aproveita a simetria, requer menos armazenamento e aproximadamente metade do trabalho de uma LU genérica. Antes de utilizá-la, deve-se verificar simetria e positividade. Tentar esconder uma falha adicionando um pequeno valor à diagonal muda o problema e precisa ser explicitamente justificado.

## Sistemas tridiagonais

Matrizes tridiagonais aparecem em discretizações de equações diferenciais. O algoritmo de Thomas explora a estrutura e resolve o sistema em $O(n)$, enquanto uma eliminação densa desperdiçaria trabalho e memória. Esse é um exemplo de princípio geral: conhecer a estrutura do problema pode ser mais importante que escolher a implementação genérica mais sofisticada.

## Condicionamento e matriz de Hilbert

Matrizes de Hilbert são exemplos clássicos de sistemas mal-condicionados. Mesmo que o resíduo calculado seja pequeno, os coeficientes da solução podem apresentar erro relevante. O experimento deve comparar precisão, número de condição e erro na solução, não apenas o resíduo.

## PageRank como sistema linear

Em uma rede de páginas, o PageRank pode ser formulado como um sistema que combina a matriz de transição com um fator de amortecimento. O exemplo conecta álgebra linear, grafos e métodos numéricos. Também mostra que modelagem influencia condicionamento: alterar amortecimento e conectividade muda a sensibilidade e a velocidade dos métodos.

# Sistemas lineares: métodos iterativos

## Decomposição e ideia básica

Escrevendo $A=D-L-U$, os métodos estacionários constroem sequências da forma

$$x^{(k+1)}=T x^{(k)}+c.$$

A convergência para qualquer ponto inicial ocorre quando o raio espectral satisfaz $\rho(T)<1$. Critérios como dominância diagonal e o critério de Sassenfeld são condições suficientes úteis, mas não equivalem à condição espectral.

## Gauss-Jacobi e Gauss-Seidel

Jacobi calcula todas as componentes novas usando somente valores da iteração anterior. Gauss-Seidel utiliza imediatamente os valores já atualizados. Essa diferença costuma acelerar a convergência de Gauss-Seidel, embora o resultado dependa da matriz e da ordenação das equações.

Jacobi possui paralelismo natural. Gauss-Seidel introduz dependências dentro da iteração. Em problemas grandes, a escolha pode envolver não apenas quantidade de iterações, mas arquitetura computacional, comunicação e memória.

## SOR

O método de sobre-relaxação combina o valor antigo com a atualização de Gauss-Seidel. Para um parâmetro $\omega$,

$$x_i^{(k+1)}=(1-\omega)x_i^{(k)}+\omega\,\widetilde{x}_i^{(k+1)}.$$

Quando $1<\omega<2$, a sobre-relaxação pode acelerar a convergência; valores inadequados podem piorá-la ou provocar divergência. O parâmetro deve ser estudado experimentalmente ou estimado a partir da estrutura do problema.

## Gradiente conjugado

Para matrizes simétricas definidas positivas, o gradiente conjugado busca a solução em subespaços de Krylov e minimiza uma função quadrática associada. Em aritmética exata, terminaria em no máximo $n$ passos, mas em ponto flutuante sua velocidade depende fortemente da distribuição dos autovalores e de $\kappa(A)$.

O pré-condicionamento substitui o sistema por uma forma equivalente mais favorável numericamente. Um bom pré-condicionador aproxima $A$, é barato de aplicar e reduz a dispersão espectral.

## Equação do calor como projeto integrador

Ao discretizar a equação de calor estacionária em uma dimensão, obtém-se um sistema tridiagonal. Esse problema permite comparar Thomas, métodos estacionários e gradiente conjugado, além de observar como o refinamento da malha altera dimensão, condicionamento e custo.

> **Leitura dos resultados.** Não compare métodos apenas por tempo em uma única matriz. Registre dimensão, tolerância, número de iterações, norma do resíduo, estrutura da matriz e ambiente de execução.

# Interpolação polinomial e splines

## O problema de interpolação

Dados $n+1$ pontos com abscissas distintas, existe um único polinômio de grau no máximo $n$ que passa por todos eles. As formas de Lagrange e Newton representam esse mesmo polinômio, mas possuem características computacionais diferentes.

Na forma de Lagrange,

$$p_n(x)=\sum_{i=0}^{n} y_i L_i(x),\qquad L_i(x)=\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}.$$

A forma é conceitualmente direta, mas adicionar um novo ponto exige reorganizar todas as bases.

## Diferenças divididas de Newton

Newton escreve

$$p_n(x)=c_0+c_1(x-x_0)+\cdots+c_n\prod_{j=0}^{n-1}(x-x_j),$$

em que os coeficientes são diferenças divididas. Ao acrescentar um ponto, os coeficientes anteriores permanecem e apenas um novo termo é calculado. Isso é especialmente útil quando os dados chegam progressivamente.

## Fenômeno de Runge

Aumentar o grau com nós igualmente espaçados não garante melhora uniforme. Para certas funções, surgem oscilações intensas nas extremidades do intervalo. Nós de Chebyshev concentram pontos próximos às bordas e reduzem o máximo do produto que controla o erro de interpolação.

O ensinamento é mais amplo: mais parâmetros podem piorar uma aproximação quando a geometria do problema é ignorada.

## Splines cúbicas

Splines constroem polinômios de baixo grau em subintervalos e impõem continuidade entre as peças. A spline cúbica combina flexibilidade local e suavidade global, evitando muitas oscilações de um polinômio único de grau elevado.

Ao escolher condições de contorno, como spline natural ou derivadas prescritas, deve-se considerar o conhecimento disponível sobre o fenômeno.

# Ajuste de curvas e mínimos quadrados

## Aproximação na presença de ruído

Interpolar força a curva a passar por cada observação. Em dados experimentais, isso pode significar ajustar também o ruído. O método dos mínimos quadrados escolhe parâmetros que minimizam

$$S(\theta)=\sum_{i=1}^{m}\left(y_i-\widehat{y}(x_i;\theta)\right)^2.$$

Para um modelo linear nos parâmetros, o problema pode ser escrito como

$$\min_\beta \|X\beta-y\|_2.$$

As equações normais $X^T X\beta=X^T y$ são didáticas, mas podem piorar o condicionamento porque $\kappa(X^T X)$ é aproximadamente $\kappa(X)^2$. Fatorações QR são preferíveis em implementações robustas.

## Resíduos e escolha do modelo

Um erro global pequeno não garante um modelo adequado. O gráfico de resíduos deve parecer sem padrão sistemático. Curvatura remanescente, variância crescente ou blocos de sinais iguais indicam estrutura não capturada.

O grau de um polinômio deve equilibrar viés e variância. Métricas em dados de validação, análise física e simplicidade interpretável são mais confiáveis que aumentar o grau até o erro de treinamento quase desaparecer.

## Linearização de modelos

Modelos como $y=a e^{bx}$ ou $y=a x^b$ podem ser linearizados com logaritmos. A transformação facilita o ajuste, mas muda a estrutura do erro. Minimizar desvios no espaço logarítmico não é igual a minimizar desvios na escala original. A decisão deve ser registrada e validada nas duas escalas relevantes.

## Interpolação ou regressão?

- use interpolação quando os valores forem considerados exatos e for necessário reproduzi-los;
- use regressão quando houver ruído e o objetivo for estimar uma tendência;
- use splines suavizadoras quando se desejar flexibilidade local sem atravessar cada observação;
- reserve um conjunto de validação quando a meta for previsão.

# Diferenciação numérica

## Diferenças finitas

Expansões de Taylor produzem fórmulas progressiva, regressiva e central. As aproximações de dois pontos são

$$f'(x)\approx\frac{f(x+h)-f(x)}{h},$$

$$f'(x)\approx\frac{f(x)-f(x-h)}{h},$$

$$f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.$$

As duas primeiras possuem erro de truncamento $O(h)$. A fórmula central possui erro $O(h^2)$ porque a simetria cancela o termo de primeira ordem no erro.

## Escolha do passo

Reduzir $h$ melhora o erro de truncamento, mas amplifica arredondamento e cancelamento. O gráfico de erro em escala logarítmica costuma apresentar uma região descendente, um mínimo e depois crescimento. O melhor passo depende da precisão da máquina, da escala de $x$ e das derivadas da função.

## Dados tabelados

Quando existem apenas medições, a posição do ponto determina a fórmula disponível. Nas extremidades usam-se fórmulas unilaterais; no interior, fórmulas centrais costumam ser mais precisas. Passos não uniformes exigem fórmulas específicas ou diferenciação de um interpolador local.

## Segunda derivada e extrapolação

Uma aproximação central clássica é

$$f''(x)\approx\frac{f(x+h)-2f(x)+f(x-h)}{h^2}.$$

A extrapolação de Richardson combina aproximações obtidas com passos diferentes para cancelar o termo dominante do erro. Ela é poderosa quando a expansão assintótica é válida, mas não corrige dados ruidosos nem falhas de regularidade.

# Integração numérica

## Newton-Cotes compostas

A regra dos trapézios composta aproxima a função por segmentos lineares. Para passo uniforme $h=(b-a)/n$,

$$T_n=h\left[\frac{f(a)+f(b)}{2}+\sum_{i=1}^{n-1}f(a+ih)\right].$$

Seu erro global, sob hipóteses de suavidade, é $O(h^2)$. A regra de Simpson combina parábolas e, para $n$ par, tem erro global $O(h^4)$:

$$S_n=\frac{h}{3}\left[f(x_0)+f(x_n)+4\sum_{i\,\text{ímpar}}f(x_i)+2\sum_{i\,\text{par},\,i\ne0,n}f(x_i)\right].$$

## Quadratura de Gauss

Em vez de usar pontos igualmente espaçados, a quadratura gaussiana escolhe nós e pesos para maximizar o grau de exatidão. Uma regra de Gauss-Legendre com $n$ pontos integra exatamente polinômios de grau até $2n-1$ no intervalo padrão, antes da transformação de variável.

O método é especialmente eficiente quando a função pode ser avaliada em pontos arbitrários. Para dados tabelados fixos, trapézios, Simpson ou integração de um interpolador são mais naturais.

## Integração de dados experimentais

Ao integrar medições, não existe acesso livre a $f(x)$. É necessário respeitar a malha, o ruído e unidades. O resultado deve incluir análise dimensional e, quando possível, propagação de incerteza.

## Aplicações integradoras

Comprimento de curva, trabalho de uma força variável e probabilidade sob a densidade normal conectam quadratura a problemas geométricos, físicos e estatísticos. Cada aplicação exige mais que aplicar uma fórmula: é preciso construir o integrando, definir limites e conferir unidades ou normalização.

# Projetos reprodutíveis em Python

## Separação de responsabilidades

Uma implementação clara separa o algoritmo da coleta de dados, da geração de gráficos e da interface. Funções numéricas devem receber parâmetros explícitos e retornar solução, diagnóstico e histórico. Evite depender de variáveis globais ou imprimir como única forma de saída.

Um retorno útil para um método iterativo pode conter aproximação final, convergência, motivo de parada, iterações, resíduo e sequência de erros. Esse desenho permite produzir tabelas e gráficos sem duplicar o algoritmo.

## Testes numéricos

- casos pequenos com solução analítica;
- comparação com bibliotecas de referência;
- matrizes singulares, quase singulares e mal-condicionadas;
- variação sistemática de passo, tolerância e dimensão;
- testes das hipóteses exigidas, como simetria ou dominância diagonal;
- conferência de unidades e escalas dos dados.

## Gráficos que respondem perguntas

Um gráfico deve explicitar o que está sendo comparado. Use eixos logarítmicos para ordens de convergência e leis de escala. Identifique norma, dimensão, tolerância e método. Evite curvas sem rótulo ou uma escala que esconda a diferença relevante.

## Reprodutibilidade

Registre versão das dependências, semente aleatória, dados de entrada e ambiente de execução. Salve resultados intermediários que sustentem tabelas. O relatório deve permitir reconstruir cada conclusão a partir do código e dos dados.

# Guia de escolha de métodos

## Perguntas antes de programar

- o problema é bem ou mal-condicionado?
- a matriz é densa, esparsa, simétrica, definida positiva ou tridiagonal?
- existe derivada analítica e ela é estável?
- os dados são exatos ou ruidosos?
- quantas vezes o problema será resolvido com dados diferentes?
- qual precisão é necessária e como ela será verificada?
- há restrição de memória, paralelismo ou tempo?

## Mapa de decisão

Para uma raiz escalar com intervalo confiável, bisseção oferece segurança; Newton ou secante aceleram quando há boa inicialização. Para sistemas densos moderados, fatorações diretas são adequadas; para sistemas grandes e esparsos, métodos iterativos e pré-condicionamento tornam-se essenciais. Para dados exatos e poucos pontos, interpolação é natural; para dados ruidosos, ajuste é mais coerente. Para integrar uma função suave e avaliável, quadratura gaussiana é eficiente; para tabelas, métodos compostos respeitam a informação disponível.

## O que relatar

Todo resultado numérico deve informar método, parâmetros, critério de parada, erro ou resíduo, custo observado e hipóteses verificadas. Quando dois métodos forem comparados, use a mesma tolerância e a mesma definição de sucesso.

# Roteiro de revisão e exercícios

## Revisão conceitual

- explique a diferença entre erro e resíduo;
- dê um exemplo de problema mal-condicionado resolvido por um algoritmo estável;
- justifique por que pivoteamento parcial melhora a eliminação de Gauss;
- relacione raio espectral e convergência de uma iteração estacionária;
- explique por que nós de Chebyshev reduzem o fenômeno de Runge;
- compare interpolação e ajuste de curvas na presença de ruído;
- descreva o conflito entre truncamento e arredondamento na derivação numérica;
- indique quando quadratura gaussiana não é apropriada.

## Exercícios computacionais

- implemente bisseção, Newton e secante com uma interface de diagnóstico comum;
- compare Gauss com e sem pivoteamento em precisão simples;
- meça o custo de LU quando a matriz é reutilizada para muitos vetores $b$;
- compare Jacobi, Gauss-Seidel, SOR e gradiente conjugado em uma matriz SPD;
- reproduza o fenômeno de Runge com nós uniformes e de Chebyshev;
- ajuste modelos de graus diferentes e analise resíduos em dados de validação;
- trace erro de diferenças finitas em função de $h$;
- estime uma integral por trapézios, Simpson e Gauss-Legendre usando o mesmo orçamento de avaliações.

## Critério de conclusão

Uma solução está pronta quando o código executa, as hipóteses foram verificadas, o erro foi medido, os resultados podem ser reproduzidos e a interpretação distingue propriedades do problema de propriedades do algoritmo.


# Cadernos de investigação computacional

O PDF final incorpora, sem alteração, os quatro relatórios acadêmicos listados em `../fontes.md`.
