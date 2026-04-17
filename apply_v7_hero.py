import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V6 in comments
content = content.replace("<!-- V6 HERO CENTERPIECE DEPTH START -->", "{% comment %}\n<!-- V6 HERO CENTERPIECE DEPTH START -->")
content = content.replace("<!-- V6 HERO CENTERPIECE DEPTH END -->", "<!-- V6 HERO CENTERPIECE DEPTH END -->\n{% endcomment %}")

# Prepare V7 (Opção 4 - Editorial Split Design)
v7_html = """
<!-- V7 HERO EDITORIAL SPLIT START -->
<div class="relative w-full h-[80vh] lg:h-[90vh] overflow-hidden bg-white flex" x-data="heroSliderV7()" x-init="start()">

    <template x-for="(slide, index) in slides" :key="index">
        <div class="absolute inset-0 w-full h-full flex flex-col lg:flex-row"
             x-show="active === index"
             x-transition:enter="transition-transform duration-[1200ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
             x-transition:enter-start="opacity-0 translate-x-32"
             x-transition:enter-end="opacity-100 translate-x-0"
             x-transition:leave="transition-transform duration-[800ms] ease-in"
             x-transition:leave-start="opacity-100 translate-x-0"
             x-transition:leave-end="opacity-0 -translate-x-32">

            <!-- LEFT SIDE: Text Editorial -->
            <div class="lg:w-1/2 w-full h-full flex flex-col justify-center px-8 lg:px-24 bg-white relative z-20">
                
                <div x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-[400ms] ease-out"
                     x-transition:enter-start="opacity-0 translate-y-8"
                     x-transition:enter-end="opacity-100 translate-y-0">
                    <p class="text-[11px] font-bold tracking-[0.3em] uppercase text-gray-400 mb-8 flex items-center gap-4">
                        <span class="w-10 h-px bg-gray-300"></span>
                        <span x-text="slide.subtitle"></span>
                    </p>
                </div>

                <div x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-[550ms] ease-out"
                     x-transition:enter-start="opacity-0 translate-y-8"
                     x-transition:enter-end="opacity-100 translate-y-0"
                     class="mb-8">
                    <h2 class="text-5xl md:text-6xl lg:text-[5rem] font-black leading-[1.05] tracking-tight text-gray-900" x-html="slide.title"></h2>
                </div>

                <div x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-[700ms] ease-out"
                     x-transition:enter-start="opacity-0 translate-y-8"
                     x-transition:enter-end="opacity-100 translate-y-0"
                     class="mb-12 max-w-md">
                    <p class="text-base text-gray-500 font-normal leading-loose" x-text="slide.description"></p>
                </div>

                <div x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-[850ms] ease-out"
                     x-transition:enter-start="opacity-0 translate-y-8"
                     x-transition:enter-end="opacity-100 translate-y-0">
                    <a :href="slide.link" class="group relative inline-flex items-center justify-center px-10 py-5 bg-black text-white overflow-hidden rounded-sm hover:-translate-y-1 transition-transform duration-300">
                        <span class="absolute w-0 h-0 transition-all duration-500 ease-out bg-primary rounded-full group-hover:w-72 group-hover:h-56"></span>
                        <span class="relative text-xs font-bold tracking-[0.2em] uppercase z-10 flex items-center gap-3">
                            <span x-text="slide.cta"></span>
                            <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                        </span>
                    </a>
                </div>
            </div>

            <!-- RIGHT SIDE: Product Studio (Soft Color Block Split) -->
            <div class="lg:w-1/2 w-full h-[50vh] lg:h-full relative flex items-center justify-center overflow-hidden" :class="slide.bgColor">
                
                <!-- Floating Ambient Circle back element -->
                <div class="absolute w-[80%] h-[80%] rounded-full bg-white/40 blur-3xl mix-blend-overlay"></div>

                <!-- Product Image -->
                <img :src="slide.image"
                     :alt="slide.title"
                     class="relative z-10 w-[90%] lg:w-[100%] max-w-[650px] object-contain drop-shadow-[0_30px_30px_rgba(0,0,0,0.1)]"
                     x-show="active === index"
                     x-transition:enter="transition-all duration-[1200ms] delay-[500ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
                     x-transition:enter-start="opacity-0 translate-y-16 scale-95"
                     x-transition:enter-end="opacity-100 translate-y-0 scale-100">
            </div>

        </div>
    </template>

    <!-- Bottom Left Minimal Nav / Controller -->
    <div class="absolute bottom-0 left-0 w-full lg:w-1/2 px-8 lg:px-24 pb-12 z-30 flex items-center justify-between border-t border-gray-100 bg-white/80 backdrop-blur-sm lg:bg-transparent lg:border-t-0 lg:backdrop-blur-none">
        <!-- Lines Progress -->
        <div class="flex items-center gap-4">
            <template x-for="(slide, idx) in slides" :key="idx">
                <button @click="goTo(idx)" class="group cursor-pointer py-4 flex items-center">
                    <div class="h-[2px] transition-all duration-500 rounded-none relative overflow-hidden"
                         :class="active === idx ? 'w-16 bg-gray-200' : 'w-8 bg-gray-200 group-hover:bg-gray-300'">
                        <div x-show="active === idx" class="absolute inset-y-0 left-0 bg-black h-full transition-all duration-75" :style="`width: ${progress}%`"></div>
                    </div>
                </button>
            </template>
        </div>

        <div class="flex items-center gap-1">
            <button @click="prev()" class="w-12 h-12 flex items-center justify-center text-gray-400 hover:text-black border border-transparent hover:border-gray-200 transition-all duration-300 rounded-sm">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"></path></svg>
            </button>
            <button @click="next()" class="w-12 h-12 flex items-center justify-center text-gray-400 hover:text-black border border-transparent hover:border-gray-200 transition-all duration-300 rounded-sm">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5l7 7-7 7"></path></svg>
            </button>
        </div>
    </div>

</div>
<!-- V7 HERO EDITORIAL SPLIT END -->
"""
content = content.replace("<!-- V6 HERO CENTERPIECE DEPTH END -->\n{% endcomment %}", "<!-- V6 HERO CENTERPIECE DEPTH END -->\n{% endcomment %}\n\n" + v7_html)

# Add heroSliderV7 script
v7_script = """
    function heroSliderV7() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Evolução em PDV',
                    title: 'Totem<br>Triedro.',
                    description: 'Engajamento 360 Graus. Um totem de 3 faces focado em garantir máxima visibilidade dentro de corredores de shopping e supermercados.',
                    image: "{% static 'img/totem_triedro.png' %}?v=13",
                    cta: 'Comprar Totem',
                    link: '/produto/totem-triedro-em-poliondas/',
                    bgColor: 'bg-[#f0f4f8]'
                },
                {
                    subtitle: 'Impacto Geométrico',
                    title: 'Cubo<br>Promo.',
                    description: 'Volume estratégico que atrai os olhos automaticamente. Caixas empilháveis para montagem de ilhas promocionais criativas.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=7",
                    cta: 'Descobrir Produto',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    bgColor: 'bg-[#fcf5eb]'
                },
                {
                    subtitle: 'Praticidade Elegante',
                    title: 'Banner<br>Rollup.',
                    description: 'O parceiro ideal para apresentações. Display automontável em menos de 1 minuto que transforma qualquer feira em um estande premium.',
                    image: "{% static 'img/rollup_hero.png' %}?v=5",
                    cta: 'Configurar Agora',
                    link: '/produto/banner-rollup/',
                    bgColor: 'bg-[#f4f0f6]'
                }
            ],
            start() {
                this.resetInterval();
            },
            resetInterval() {
                clearInterval(this.interval);
                clearInterval(this.progressInterval);
                this.progress = 0;

                this.progressInterval = setInterval(() => {
                    this.progress += (100 / (7500 / 16)); 
                    if (this.progress > 100) this.progress = 100;
                }, 16);

                this.interval = setInterval(() => {
                    this.active = (this.active + 1) % this.slides.length;
                    this.resetInterval();
                }, 7500);
            },
            goTo(index) {
                this.active = index;
                this.resetInterval();
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
content = content.replace("</script>", v7_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V7 HERO Editorial Split successfully!")
