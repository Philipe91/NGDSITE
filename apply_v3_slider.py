import os

file_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\home.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I want to replace the V2 block with V3 block
# Find V2 block
start_v2 = "<!-- V2 HERO MODERNO START -->"
end_v2 = "<!-- V2 HERO MODERNO END -->"

if start_v2 in content and end_v2 in content:
    idx_start = content.find(start_v2)
    idx_end = content.find(end_v2) + len(end_v2)
    
    pre_content = content[:idx_start]
    post_content = content[idx_end:]
    
    v3_html = """
<!-- V3 HERO CLEAN & MINIMALIST START -->
<div class="relative w-full h-[70vh] lg:h-[85vh] overflow-hidden bg-[#f4f7f6]" x-data="heroSliderV3()" x-init="start()">

    <!-- Fundo Tipográfico Animado (Tamanho gigante e bem leve no fundo) -->
    <div class="absolute inset-0 z-0 flex items-center justify-center overflow-hidden pointer-events-none opacity-[0.03]">
        <template x-for="(slide, index) in slides" :key="index">
            <h1 x-show="active === index"
                x-transition:enter="transition-all duration-1000 ease-out"
                x-transition:enter-start="opacity-0 scale-90 translate-y-10"
                x-transition:enter-end="opacity-100 scale-100 translate-y-0"
                class="text-[15rem] md:text-[25rem] font-black uppercase text-black whitespace-nowrap"
                x-text="slide.bigBgText"></h1>
        </template>
    </div>

    <!-- Bolha dinâmica de cor (Glow) que acompanha o fundo de forma super suave -->
    <template x-for="(slide, index) in slides" :key="'glow'+index">
        <div x-show="active === index"
             x-transition:enter="transition ease-out duration-[3000ms]"
             x-transition:enter-start="opacity-0 scale-50"
             x-transition:enter-end="opacity-100 scale-100"
             class="absolute top-1/2 right-[10%] -translate-y-1/2 w-[40rem] h-[40rem] rounded-full blur-[120px] pointer-events-none z-0"
             :class="slide.glowColor"></div>
    </template>

    <div class="absolute inset-0 w-full h-full z-10 flex">
        <template x-for="(slide, index) in slides" :key="index">
            <div class="w-full h-full flex items-center" x-show="active === index">
                
                <div class="container mx-auto px-4 lg:px-8">
                    <div class="grid lg:grid-cols-12 gap-12 items-center w-full mt-10 md:mt-0">
                        
                        <!-- Conteúdo Esquerdo (Textos Escuros em Fundo Claro) -->
                        <div class="lg:col-span-6 flex flex-col justify-center relative z-20 md:pr-10">
                            
                            <!-- Etiqueta de Lançamento -->
                            <div x-show="active === index"
                                 x-transition:enter="transition ease-out duration-[1200ms] delay-100"
                                 x-transition:enter-start="opacity-0 -translate-x-10"
                                 x-transition:enter-end="opacity-100 translate-x-0">
                                <span class="inline-block py-2 px-5 rounded-full bg-white border border-gray-200 text-primary text-[10px] md:text-xs font-bold tracking-[0.2em] uppercase mb-8 shadow-sm">
                                    <span class="w-2 h-2 rounded-full inline-block bg-primary mr-2 animate-pulse"></span>
                                    <span x-text="slide.subtitle"></span>
                                </span>
                            </div>

                            <!-- Título Principal com cor -->
                            <div x-show="active === index"
                                 x-transition:enter="transition ease-out duration-[1200ms] delay-300"
                                 x-transition:enter-start="opacity-0 -translate-x-10"
                                 x-transition:enter-end="opacity-100 translate-x-0">
                                <h2 class="text-5xl md:text-6xl lg:text-[4.5rem] font-extrabold text-[#111827] leading-[1.1] tracking-tight mb-6" x-html="slide.title"></h2>
                            </div>

                            <!-- Parágrafo -->
                            <div x-show="active === index"
                                 x-transition:enter="transition ease-out duration-[1200ms] delay-500"
                                 x-transition:enter-start="opacity-0 -translate-x-10"
                                 x-transition:enter-end="opacity-100 translate-x-0">
                                <p class="text-lg md:text-xl text-gray-500 mb-10 max-w-lg font-normal leading-relaxed" x-text="slide.description"></p>
                            </div>
                            
                            <!-- Botões de Ação -->
                            <div x-show="active === index"
                                 x-transition:enter="transition ease-out duration-[1200ms] delay-700"
                                 x-transition:enter-start="opacity-0 translate-y-6"
                                 x-transition:enter-end="opacity-100 translate-y-0">
                                <div class="flex flex-wrap gap-4 items-center">
                                    <a :href="slide.link" class="group relative inline-flex items-center justify-center px-8 md:px-10 py-4 font-bold text-white bg-primary rounded-full overflow-hidden transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-primary/30">
                                        <span class="relative z-10 uppercase tracking-widest text-[13px]" x-text="slide.cta"></span>
                                        <svg class="w-4 h-4 ml-3 relative z-10 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                                    </a>
                                    
                                    <!-- Play btn fake / Ver video (opcional p/ dar modernidade) -->
                                    <button class="w-14 h-14 rounded-full bg-white border border-gray-200 text-gray-800 flex items-center justify-center hover:bg-gray-50 hover:scale-110 transition-transform shadow-sm group">
                                        <svg class="w-5 h-5 ml-1 text-primary group-hover:text-secondary transition-colors" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Lado da Imagem (mix-blend-multiply dissolve qualquer fundo branco de imagem jpg/png) -->
                        <div class="lg:col-span-6 relative z-20 hidden md:flex items-center justify-center lg:justify-end h-[500px]">
                            <img :src="slide.image" 
                                 :alt="slide.title"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-[1500ms] ease-out delay-300"
                                 x-transition:enter-start="opacity-0 translate-x-32 translate-y-10 scale-90 -rotate-3"
                                 x-transition:enter-end="opacity-100 translate-x-0 translate-y-0 scale-100 rotate-0"
                                 x-transition:leave="transition-all duration-[800ms] ease-in"
                                 x-transition:leave-start="opacity-100 translate-x-0 scale-100"
                                 x-transition:leave-end="opacity-0 -translate-x-32 scale-95"
                                 class="relative w-[110%] max-w-3xl object-contain drop-shadow-2xl mix-blend-multiply">
                        </div>

                    </div>
                </div>
            </div>
        </template>
    </div>

    <!-- Controles de Progressão Estilo "Timeline" (Inferior Esquerdo) -->
    <div class="absolute bottom-8 lg:bottom-12 left-6 lg:left-12 z-30 flex items-center gap-6">
        <template x-for="(slide, idx) in slides" :key="idx">
            <button @click="goTo(idx)" class="group flex flex-col gap-2">
                <span class="text-[10px] uppercase tracking-widest font-bold transition-colors"
                      :class="active === idx ? 'text-primary' : 'text-gray-400 group-hover:text-gray-600'"
                      x-text="'0' + (idx + 1)"></span>
                <div class="h-1 rounded-full bg-gray-200 transition-all overflow-hidden"
                     :class="active === idx ? 'w-16' : 'w-8 group-hover:w-10'">
                     <!-- Barra enchendo apenas no item ativo -->
                     <div x-show="active === idx" class="h-full bg-primary" :style="`width: ${progress}%`"></div>
                </div>
            </button>
        </template>
    </div>

    <!-- Setas de controle Laterais Direita -->
    <div class="absolute bottom-8 lg:bottom-12 right-6 lg:right-12 z-30 flex gap-2">
        <button @click="prev()" class="w-12 h-12 bg-white rounded-full flex items-center justify-center text-gray-800 shadow-md hover:scale-110 hover:shadow-lg hover:text-primary transition-all border border-gray-100">
            <svg class="w-5 h-5 -ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        </button>
        <button @click="next()" class="w-12 h-12 bg-white rounded-full flex items-center justify-center text-gray-800 shadow-md hover:scale-110 hover:shadow-lg hover:text-primary transition-all border border-gray-100">
            <svg class="w-5 h-5 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>
    </div>

</div>
<!-- V3 HERO CLEAN & MINIMALIST END -->
"""
    
    # We need to add heroSliderV3 JS func
    v3_js = """
    function heroSliderV3() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Novo Produto',
                    title: 'Totem <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-blue-400">Elíptico</span>',
                    description: 'Elegância minimalista. Totem de montagem expressa que revoluciona o layout da sua loja com impressão fotográfica.',
                    image: "{% static 'img/totem_ptbr.png' %}",
                    cta: 'Personalizar',
                    link: '/produto/totem-eliptico/',
                    bigBgText: 'TOTEM',
                    glowColor: 'bg-blue-300/30'
                },
                {
                    subtitle: 'Impacto Visual',
                    title: 'Cubo <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-red-500">Promocional</span>',
                    description: 'Destaque-se em 360 graus. Excelente para vitrines dinâmicas e empilhamento em ilhas estratégicas no PDV.',
                    image: "{% static 'img/cubo_ptbr.png' %}",
                    cta: 'Ver Detalhes',
                    link: '/produto/cubo-promocional/',
                    bigBgText: 'CUBO',
                    glowColor: 'bg-orange-300/20'
                },
                {
                    subtitle: 'Alta Conversão',
                    title: 'Wobbler <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-teal-400">Gôndola</span>',
                    description: 'A sinalização saltada da prateleira que quebra o padrão visual e captura a atenção imediata do shopper.',
                    image: "{% static 'img/wobbler_ptbr.png' %}",
                    cta: 'Conhecer',
                    link: '/produto/wobbler/',
                    bigBgText: 'WOBBLER',
                    glowColor: 'bg-green-300/20'
                }
            ],
            start() {
                this.resetInterval();
            },
            resetInterval() {
                clearInterval(this.interval);
                clearInterval(this.progressInterval);
                this.progress = 0;

                // 8000ms total
                this.progressInterval = setInterval(() => {
                    this.progress += 1;
                    if (this.progress > 100) this.progress = 100;
                }, 80);

                this.interval = setInterval(() => {
                    this.next();
                }, 8000);
            },
            next() {
                this.active = (this.active + 1) % this.slides.length;
                this.resetInterval();
            },
            prev() {
                this.active = (this.active - 1 + this.slides.length) % this.slides.length;
                this.resetInterval();
            },
            goTo(index) {
                this.active = index;
                this.resetInterval();
            }
        }
    }
"""
    
    content = pre_content + v3_html + post_content
    
    if "function heroSliderV3()" not in content:
        content = content.replace("</script>", v3_js + "\n</script>\n")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("V3 aplicada!")

