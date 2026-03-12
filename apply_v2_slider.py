import os
import django

file_path = r"C:\Users\Pc Fechamento\Documents\NGDSITE\templates\catalog\home.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I want to add V2 before `<!-- FEATURES SECTION -->`
split_marker = r"<!-- FEATURES SECTION -->"
parts = content.split(split_marker)

if len(parts) >= 2:
    header_part = parts[0]
    
    # Check if we already wrapped in comment
    if "{% comment %}" not in header_part:
        # Replace the start of Hero
        header_part = header_part.replace("<!-- HERO SLIDER SECTION -->", "<!-- HERO SLIDER SECTION -->\n{% comment %}")
        header_part = header_part + "{% endcomment %}\n\n"
        
        v2_html = """
<!-- V2 HERO MODERNO START -->
<div class="relative w-full h-[70vh] lg:h-[85vh] overflow-hidden bg-[#001730]" x-data="heroSliderV2()" x-init="start()">
    
    <template x-for="(slide, index) in slides" :key="index">
        <div class="absolute inset-0 w-full h-full" x-show="active === index">
            
            <!-- Imagem de Fundo c/ Efeito Ken Burns Lento -->
            <div class="absolute inset-0 w-full h-full opacity-40 transition-transform duration-[10000ms] ease-linear"
                 :class="active === index ? 'scale-110' : 'scale-100'">
                <div class="absolute inset-0 bg-gradient-to-br from-[#000a18] via-[#001f4d] to-[#003366]"></div>
            </div>

            <div class="absolute inset-0 container mx-auto px-4 lg:px-8 flex items-center">
                <div class="grid lg:grid-cols-12 gap-8 w-full mt-10 md:mt-0">
                    
                    <!-- Content (Left) -->
                    <div class="lg:col-span-6 flex flex-col justify-center relative z-20">
                        <div x-show="active === index"
                             x-transition:enter="transition ease-out duration-1000 delay-200 transform"
                             x-transition:enter-start="opacity-0 -translate-x-12"
                             x-transition:enter-end="opacity-100 translate-x-0">
                            <span class="inline-block py-1.5 px-4 rounded-full bg-white/10 text-white backdrop-blur-md border border-white/20 text-xs font-bold tracking-[0.2em] uppercase mb-6" x-text="slide.subtitle"></span>
                        </div>

                        <div x-show="active === index"
                             x-transition:enter="transition ease-out duration-1000 delay-400 transform"
                             x-transition:enter-start="opacity-0 -translate-x-12"
                             x-transition:enter-end="opacity-100 translate-x-0">
                            <h2 class="text-5xl md:text-6xl lg:text-[5rem] font-bold text-white leading-[1.05] tracking-tight mb-6 drop-shadow-2xl" x-html="slide.title"></h2>
                        </div>

                        <div x-show="active === index"
                             x-transition:enter="transition ease-out duration-1000 delay-600 transform"
                             x-transition:enter-start="opacity-0 -translate-x-12"
                             x-transition:enter-end="opacity-100 translate-x-0">
                            <p class="text-lg md:text-xl text-gray-300 mb-10 max-w-xl font-light leading-relaxed drop-shadow-md" x-text="slide.description"></p>
                        </div>
                        
                        <div x-show="active === index"
                             x-transition:enter="transition ease-out duration-1000 delay-800 transform"
                             x-transition:enter-start="opacity-0 -translate-x-12 translate-y-4"
                             x-transition:enter-end="opacity-100 translate-x-0 translate-y-0">
                            <a :href="slide.link" class="group relative inline-flex items-center justify-center px-8 md:px-10 py-4 font-bold text-white bg-white/10 backdrop-blur-lg border border-white/30 rounded-full overflow-hidden transition-all hover:bg-white/20 hover:scale-105 hover:shadow-[0_0_40px_rgba(255,255,255,0.3)] hover:border-white/60">
                                <span class="relative z-10 uppercase tracking-widest text-sm" x-text="slide.cta"></span>
                                <svg class="w-4 h-4 ml-3 relative z-10 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                            </a>
                        </div>
                    </div>

                    <!-- Image (Right) -->
                    <div class="lg:col-span-6 relative z-10 hidden md:flex items-center justify-center lg:justify-end min-h-[400px]">
                        
                        <!-- Glow Effect dinâmico por trás da imagem -->
                        <div x-show="active === index"
                             x-transition:enter="transition ease-out duration-[2000ms]"
                             x-transition:enter-start="opacity-0 scale-50"
                             x-transition:enter-end="opacity-100 scale-100"
                             class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[30rem] h-[30rem] bg-blue-500/20 rounded-full blur-[100px] pointer-events-none"></div>

                        <img :src="slide.image" 
                             :alt="slide.title"
                             x-show="active === index"
                             x-transition:enter="transition ease-out duration-1000 delay-500 transform"
                             x-transition:enter-start="opacity-0 translate-x-24 scale-90 rotate-6"
                             x-transition:enter-end="opacity-100 translate-x-0 scale-100 rotate-0"
                             x-transition:leave="transition ease-in duration-500 transform"
                             x-transition:leave-start="opacity-100 translate-x-0 scale-100"
                             x-transition:leave-end="opacity-0 -translate-x-24 scale-105"
                             class="relative z-20 w-[90%] lg:w-[130%] max-w-2xl object-contain drop-shadow-[0_40px_60px_rgba(0,0,0,0.8)] mix-blend-normal">
                    </div>

                </div>
            </div>
        </div>
    </template>

    <!-- Overlay Gradiente Base -->
    <div class="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-black/80 to-transparent z-20 pointer-events-none"></div>

    <!-- Navegação Numérica e ProgressBar -->
    <div class="absolute bottom-8 md:bottom-12 left-6 md:left-12 lg:left-20 z-30 flex items-center gap-4 md:gap-6">
        <div class="text-white/50 font-mono text-xs md:text-sm tracking-widest">
            <span class="text-white text-base md:text-lg font-bold shadow-sm" x-text="String(active + 1).padStart(2, '0')"></span> <span class="mx-1">/</span> <span x-text="String(slides.length).padStart(2, '0')"></span>
        </div>
        
        <div class="w-24 md:w-48 lg:w-64 h-1.5 bg-white/20 rounded-full overflow-hidden relative shadow-sm">
            <div class="h-full bg-white transition-all duration-75 ease-linear" :style="`width: ${progress}%`"></div>
        </div>
    </div>

    <!-- Controles Next/Prev -->
    <div class="absolute bottom-8 md:bottom-12 right-6 md:right-12 lg:right-20 z-30 flex gap-2 md:gap-3">
        <button @click="prev()" class="w-10 h-10 md:w-12 md:h-12 rounded-full border border-white/30 text-white flex items-center justify-center backdrop-blur-md hover:bg-white hover:text-black hover:scale-110 transition-all shadow-lg hover:shadow-white/20">
            <svg class="w-4 h-4 md:w-5 md:h-5 -ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
        </button>
        <button @click="next()" class="w-10 h-10 md:w-12 md:h-12 rounded-full border border-white/30 text-white flex items-center justify-center backdrop-blur-md hover:bg-white hover:text-black hover:scale-110 transition-all shadow-lg hover:shadow-white/20">
            <svg class="w-4 h-4 md:w-5 md:h-5 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </button>
    </div>

</div>
<!-- V2 HERO MODERNO END -->

"""
        content = header_part + v2_html + split_marker + parts[1]

# Now we need to append `heroSliderV2` JS code before `</script>`
v2_script = """
    function heroSliderV2() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Lançamento Premium',
                    title: 'Totem<br><span class="font-light text-blue-400">Elíptico</span>',
                    description: 'Marketing Inteligente para PDV! Totem automontável em 3 segundos. Impressão de alta resolução com proteção UV e acabamento impecável.',
                    image: "{% static 'img/totem_ptbr.png' %}",
                    cta: 'Personalizar Agora',
                    link: '/produto/totem-eliptico/'
                },
                {
                    subtitle: 'Destaque no PDV',
                    title: 'Cubo<br><span class="font-light text-blue-400">Promocional</span>',
                    description: 'Gere volume e chame atenção à distância. Caixas leves e resistentes. Ideal para vitrines, ilhas e ações promocionais estratégicas.',
                    image: "{% static 'img/cubo_ptbr.png' %}",
                    cta: 'Comprar Cubo',
                    link: '/produto/cubo-promocional/'
                },
                {
                    subtitle: 'Novidade Exclusiva',
                    title: 'Wobbler<br><span class="font-light text-blue-400">Gôndola</span>',
                    description: 'O material que salta aos olhos do cliente, desenhado para anunciar seus grandes lançamentos na gôndola com impacto visual profundo.',
                    image: "{% static 'img/wobbler_ptbr.png' %}",
                    cta: 'Ver Detalhes',
                    link: '/produto/wobbler/'
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
            }
        }
    }
"""

if "function heroSliderV2()" not in content:
    content = content.replace("</script>", v2_script + "\n</script>")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Modificação V2 inserida com sucesso em {file_path}")
