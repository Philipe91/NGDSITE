import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V8 in comments (Separe ele)
content = content.replace("<!-- V8 HERO GLAZED MESH START -->", "{% comment %}\n<!-- V8 HERO GLAZED MESH START -->")
content = content.replace("<!-- V8 HERO GLAZED MESH END -->", "<!-- V8 HERO GLAZED MESH END -->\n{% endcomment %}")

# Prepare V9 (Opção 6 - Museum Showcase / Presentation Pedestal)
v9_html = """
<!-- V9 HERO MUSEUM SHOWCASE START -->
<div class="relative w-full h-[85vh] lg:h-[95vh] overflow-hidden bg-gray-50 font-sans" x-data="heroSliderV9()" x-init="start()">

    <!-- Studio Lighting Background -->
    <!-- Top Spotlight -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[50%] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-white/90 via-transparent to-transparent pointer-events-none z-0"></div>
    
    <!-- Floor Horizon Line & Floor Gradient -->
    <div class="absolute bottom-0 left-0 w-full h-[35%] bg-gradient-to-t from-gray-200/50 to-transparent border-t border-gray-100/50 pointer-events-none z-0"></div>

    <div class="absolute inset-0 w-full h-full z-10 flex">
        <template x-for="(slide, index) in slides" :key="index">
            <div class="absolute inset-0 w-full h-full flex items-center justify-center pt-10"
                 x-show="active === index"
                 x-transition:enter="transition-all ease-[cubic-bezier(0.22,1,0.36,1)] duration-[1200ms]"
                 x-transition:enter-start="opacity-0"
                 x-transition:enter-end="opacity-100"
                 x-transition:leave="transition-all ease-in-out duration-[800ms] z-0"
                 x-transition:leave-start="opacity-100"
                 x-transition:leave-end="opacity-0">

                <div class="container mx-auto px-4 lg:px-8 xl:px-16 w-full h-full flex flex-col md:flex-row items-center relative gap-8">
                    
                    <!-- Left Content: Editorial Plaque -->
                    <div class="md:w-[45%] lg:w-[40%] flex flex-col justify-center relative z-30 pt-16 md:pt-0">
                        
                        <!-- Museum Plaque Line -->
                        <div class="flex items-center gap-4 mb-8"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-300"
                             x-transition:enter-start="opacity-0 translate-x-[-20px]"
                             x-transition:enter-end="opacity-100 translate-x-0">
                            <span class="w-12 h-0.5 bg-gray-900"></span>
                            <span class="text-xs font-bold uppercase tracking-[0.3em] text-gray-500" x-text="'Artigo ' + ('0'+(index+1))"></span>
                        </div>

                        <!-- Title -->
                        <div class="mb-6 relative">
                            <!-- Subtle large number behind title -->
                            <div class="absolute -top-16 -left-8 text-[12rem] font-black text-gray-900/5 select-none pointer-events-none leading-none z-[-1]"
                                 x-text="'0' + (index+1)"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-[1500ms] delay-100 ease-out"
                                 x-transition:enter-start="opacity-0 -translate-x-12"
                                 x-transition:enter-end="opacity-100 translate-x-0"></div>
                            
                            <h2 class="text-5xl md:text-6xl lg:text-[5.5rem] font-black leading-[1.05] tracking-tight text-gray-900 drop-shadow-sm"
                                x-show="active === index"
                                x-transition:enter="transition-all duration-[900ms] delay-400 ease-out"
                                x-transition:enter-start="opacity-0 translate-y-8"
                                x-transition:enter-end="opacity-100 translate-y-0"
                                x-html="slide.title"></h2>
                        </div>

                        <!-- Description -->
                        <div class="mb-12 max-w-sm"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-600 ease-out"
                             x-transition:enter-start="opacity-0 translate-y-8"
                             x-transition:enter-end="opacity-100 translate-y-0">
                            <p class="text-base text-gray-500 leading-relaxed" x-text="slide.description"></p>
                        </div>

                        <!-- Add to Cart / Action -->
                        <div class="flex items-center gap-8"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-800 ease-out"
                             x-transition:enter-start="opacity-0 translate-y-8"
                             x-transition:enter-end="opacity-100 translate-y-0">
                            <a :href="slide.link" class="group relative flex items-center justify-center bg-gray-900 text-white rounded-full w-14 h-14 hover:w-48 transition-all duration-500 overflow-hidden shadow-xl hover:shadow-2xl">
                                <!-- The Arrow (always visible initially) -->
                                <svg class="w-5 h-5 absolute group-hover:opacity-0 transition-opacity duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                                <!-- The full text (revealed on hover) -->
                                <span class="absolute whitespace-nowrap text-xs font-bold tracking-widest uppercase opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-100">
                                    <span x-text="slide.cta"></span>
                                </span>
                            </a>
                            <a :href="slide.link" class="text-sm font-bold uppercase tracking-widest text-gray-900 hover:text-primary transition-colors border-b border-gray-900 hover:border-primary pb-1">Ver Produto</a>
                        </div>
                    </div>

                    <!-- Right Content: The Showcase Pedestal -->
                    <div class="md:w-[55%] lg:w-[60%] h-[45vh] md:h-full relative flex items-center justify-center z-20">
                        
                        <!-- The Invisible Pedestal Glow -->
                        <div class="absolute bottom-[10%] w-[60%] h-[40px] rounded-[100%] blur-[20px] mix-blend-multiply opacity-50 transition-colors duration-1000 z-10" :class="slide.shadowColor"></div>
                        
                        <!-- Extra dynamic floor reflection -->
                        <div class="absolute bottom-[5%] w-[80%] h-[60px] rounded-[100%] bg-white/40 blur-[10px] scale-y-50 z-0"></div>

                        <!-- Product Standing Tall -->
                        <div class="relative w-full h-[90%] flex items-end justify-center pb-[5%] z-20">
                            <img :src="slide.image"
                                 :alt="slide.title"
                                 class="relative max-h-full max-w-[90%] object-contain drop-shadow-[0_20px_20px_rgba(0,0,0,0.1)] origin-bottom"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-[1200ms] delay-400 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
                                 x-transition:enter-start="opacity-0 scale-90 translate-y-32"
                                 x-transition:enter-end="opacity-100 scale-100 translate-y-0">
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>

    <!-- Vertical Interactive Index Navigation (Right Edge) -->
    <div class="absolute right-8 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col gap-6">
        <template x-for="(slide, idx) in slides" :key="idx">
            <button @click="goTo(idx)" 
                    class="group flex items-center gap-4 text-right focus:outline-none justify-end">
                <span class="text-[10px] font-bold uppercase tracking-[0.2em] transition-all duration-300"
                      :class="active === idx ? 'text-gray-900 translate-x-0' : 'text-gray-400 opacity-0 group-hover:opacity-100 translate-x-4'"
                      x-text="slide.navName"></span>
                <span class="w-1.5 transition-all duration-500 rounded-full"
                      :class="active === idx ? 'h-12 bg-gray-900 border border-gray-900' : 'h-2 bg-gray-300 group-hover:bg-gray-400 group-hover:h-6'"></span>
            </button>
        </template>
    </div>

    <!-- Timeline Progress Bottom Left -->
    <div class="absolute bottom-10 left-8 lg:left-16 z-40 w-48 hidden md:block">
        <div class="h-[2px] bg-gray-200 w-full overflow-hidden">
            <div class="h-full bg-gray-900 transition-all duration-[100ms] ease-linear" :style="`width: ${progress}%`"></div>
        </div>
        <div class="flex justify-between mt-3">
            <span class="text-[10px] font-bold tracking-widest text-gray-900" x-text="'0' + (active + 1)"></span>
            <span class="text-[10px] font-bold tracking-widest text-gray-400" x-text="'0' + slides.length"></span>
        </div>
    </div>

</div>
<!-- V9 HERO MUSEUM SHOWCASE END -->
"""
content = content.replace("<!-- V8 HERO GLAZED MESH END -->\n{% endcomment %}", "<!-- V8 HERO GLAZED MESH END -->\n{% endcomment %}\n\n" + v9_html)

# Add heroSliderV9 script
v9_script = """
    function heroSliderV9() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    navName: 'Totem',
                    title: 'Totem<br>Triedro.',
                    description: 'Engajamento absoluto em corredores luxuosos. Totem de 3 faces desenvolvido para presença em todos os ângulos.',
                    image: "{% static 'img/totem_triedro.png' %}?v=15",
                    cta: 'Personalizar Agora',
                    link: '/produto/totem-triedro-em-poliondas/',
                    shadowColor: 'bg-blue-900/30'
                },
                {
                    navName: 'Cubo',
                    title: 'Cubo<br>Promo.',
                    description: 'Transforme qualquer vitrine em uma obra de arte empilhável. Leve, imponente e fácil de transportar.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=9",
                    cta: 'Descobrir Cubo',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    shadowColor: 'bg-orange-900/30'
                },
                {
                    navName: 'Rollup',
                    title: 'Banner<br>Rollup.',
                    description: 'Retrátil, robusto e absurdamente elegante. A peça central de quem atrai olhares em grandes eventos.',
                    image: "{% static 'img/rollup_hero.png' %}?v=7",
                    cta: 'Configurar Layout',
                    link: '/produto/banner-rollup/',
                    shadowColor: 'bg-purple-900/30'
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
                    this.progress += (100 / (8000 / 16)); 
                    if (this.progress > 100) this.progress = 100;
                }, 16);

                this.interval = setInterval(() => {
                    this.active = (this.active + 1) % this.slides.length;
                    this.resetInterval();
                }, 8000);
            },
            goTo(index) {
                this.active = index;
                this.resetInterval();
            }
        }
    }
"""
content = content.replace("</script>", v9_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V9 HERO Museum Showcase successfully!")
