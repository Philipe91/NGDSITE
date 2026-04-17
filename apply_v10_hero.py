import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V9 in comments
content = content.replace("<!-- V9 HERO MUSEUM SHOWCASE START -->", "{% comment %}\n<!-- V9 HERO MUSEUM SHOWCASE START -->")
content = content.replace("<!-- V9 HERO MUSEUM SHOWCASE END -->", "<!-- V9 HERO MUSEUM SHOWCASE END -->\n{% endcomment %}")

# Prepare V10 (Option 7 - Neo-Bento Smart Grid)
v10_html = """
<!-- V10 HERO NEO-BENTO GRID START -->
<div class="relative w-full min-h-[90vh] lg:h-[95vh] bg-[#f0f2f5] p-4 md:p-6 lg:p-8 flex items-center justify-center font-sans tracking-tight" x-data="heroSliderV10()" x-init="start()">

    <div class="w-full max-w-[1600px] h-full flex flex-col items-center justify-center">
        
        <template x-for="(slide, index) in slides" :key="index">
            <div class="absolute inset-4 md:inset-6 lg:inset-8 w-[calc(100%-2rem)] md:w-[calc(100%-3rem)] lg:w-[calc(100%-4rem)] max-w-[1600px] mx-auto z-10"
                 x-show="active === index">
                
                <!-- Bento Grid Container -->
                <div class="grid grid-cols-1 lg:grid-cols-12 grid-rows-none lg:grid-rows-3 gap-4 lg:gap-6 w-full h-full pb-10 lg:pb-0">
                    
                    <!-- HUGE WIDGET: The Image Studio (Left side spanning 7 columns, all 3 rows) -->
                    <div class="lg:col-span-7 lg:row-span-3 h-[45vh] lg:h-full bg-white rounded-[2rem] lg:rounded-[3rem] overflow-hidden flex items-center justify-center relative shadow-sm border border-gray-100/50 group"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-[1000ms] delay-[100ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
                         x-transition:enter-start="opacity-0 translate-y-16 scale-[0.97]"
                         x-transition:enter-end="opacity-100 translate-y-0 scale-100">
                        
                        <!-- Studio Soft Spotlight -->
                        <div class="absolute top-[10%] w-[60vw] h-[60vw] rounded-full blur-[100px] opacity-40 transition-colors duration-1000 mix-blend-multiply pointer-events-none" :class="slide.colorClass"></div>
                        
                        <!-- Product Number Accent -->
                        <span class="absolute top-8 left-10 text-[10rem] font-bold text-gray-50 leading-none select-none tracking-tighter" x-text="'0' + (index+1)"></span>

                        <!-- Product Image -->
                        <img :src="slide.image"
                             :alt="slide.title"
                             class="relative w-[110%] max-w-[600px] object-contain drop-shadow-[0_20px_40px_rgba(0,0,0,0.1)] z-10 transform-gpu group-hover:scale-105 transition-transform duration-700 ease-out"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-[1200ms] delay-[400ms] ease-out"
                             x-transition:enter-start="opacity-0 scale-75 translate-y-24"
                             x-transition:enter-end="opacity-100 scale-100 translate-y-0">
                             
                        <!-- Interactive Tags Floating -->
                        <div class="absolute bottom-8 left-8 bg-white/70 backdrop-blur-md border border-white rounded-full px-5 py-2.5 shadow-lg shadow-gray-200/50 z-20 flex items-center gap-2"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-[900ms]"
                             x-transition:enter-start="opacity-0 translate-y-8"
                             x-transition:enter-end="opacity-100 translate-y-0">
                             <div class="w-1.5 h-1.5 rounded-full animate-ping" :class="'bg'+slide.colorClass.substring(2)"></div>
                             <span class="text-xs font-bold uppercase tracking-wider text-gray-800">Em Destaque</span>
                        </div>
                    </div>

                    <!-- TOP RIGHT WIDGET: Title & Copy (spanning 5 cols, 2 rows) -->
                    <div class="lg:col-span-5 lg:row-span-2 bg-white rounded-[2rem] lg:rounded-[3rem] p-8 md:p-12 shadow-sm border border-gray-100/50 flex flex-col justify-center relative overflow-hidden"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-[1000ms] delay-[200ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
                         x-transition:enter-start="opacity-0 translate-x-16"
                         x-transition:enter-end="opacity-100 translate-x-0">
                         
                        <p class="text-xs font-extrabold tracking-[0.2em] uppercase text-gray-400 mb-6 flex items-center gap-3">
                            <span class="w-5 h-1 bg-gray-900 rounded-full"></span><span x-text="slide.subtitle"></span>
                        </p>
                        <h2 class="text-5xl lg:text-6xl xl:text-7xl font-black text-gray-900 leading-[1.05] tracking-tight mb-6" x-html="slide.title"></h2>
                        <p class="text-base lg:text-lg text-gray-500 font-medium leading-relaxed max-w-md" x-text="slide.description"></p>
                    </div>

                    <!-- BOTTOM RIGHT WIDGETS -->
                    <!-- Small Widget 1: Navigation / Stats -->
                    <div class="lg:col-span-2 lg:row-span-1 bg-white rounded-[2rem] shadow-sm border border-gray-100/50 p-6 flex flex-col justify-between"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-[1000ms] delay-[300ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
                         x-transition:enter-start="opacity-0 translate-y-16"
                         x-transition:enter-end="opacity-100 translate-y-0">
                         
                         <div class="w-full flex items-center justify-between mb-4">
                             <button @click="prev()" class="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-black transition-colors">
                                 <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                             </button>
                             <button @click="next()" class="w-10 h-10 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-black transition-colors">
                                 <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                             </button>
                         </div>
                         
                         <!-- Mini Loader ring -->
                         <div class="w-full flex items-end justify-between">
                            <span class="text-6xl font-black text-gray-200 leading-none -ml-1 -mb-1" x-text="'0' + (active + 1)"></span>
                            <div class="w-8 h-8 rounded-full border-4 border-gray-100 relative mb-1">
                                <!-- Quick pure CSS circle hack based on progress -->
                                <div class="absolute inset-[-4px] rounded-full border-4 border-transparent border-t-gray-900 border-r-gray-900 transform transition-all duration-[100ms] ease-linear" :style="`transform: rotate(${progress * 3.6}deg)`"></div>
                            </div>
                         </div>
                    </div>

                    <!-- Small Widget 2: The CTA Action Block -->
                    <div class="lg:col-span-3 lg:row-span-1 rounded-[2rem] shadow-xl overflow-hidden group cursor-pointer relative"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-[1000ms] delay-[400ms] ease-[cubic-bezier(0.22,1,0.36,1)]"
                         x-transition:enter-start="opacity-0 translate-x-16"
                         x-transition:enter-end="opacity-100 translate-x-0">
                         
                        <a :href="slide.link" class="absolute inset-0 w-full h-full bg-gray-900 text-white flex flex-col justify-between p-8 group-hover:bg-primary transition-colors duration-500 z-10">
                            <!-- Top Arrow icon -->
                            <div class="flex justify-end">
                                <span class="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center group-hover:bg-white group-hover:text-primary transition-colors duration-500 group-hover:-rotate-45 transform">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                                </span>
                            </div>
                            
                            <!-- Bottom Action text -->
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-white animate-pulse"></span>
                                <h3 class="text-xl font-bold uppercase tracking-widest" x-text="slide.cta"></h3>
                            </div>
                        </a>
                    </div>
                    
                </div>
            </div>
        </template>
        
    </div>

</div>
<!-- V10 HERO NEO-BENTO GRID END -->
"""
content = content.replace("<!-- V9 HERO MUSEUM SHOWCASE END -->\n{% endcomment %}", "<!-- V9 HERO MUSEUM SHOWCASE END -->\n{% endcomment %}\n\n" + v10_html)

# Add heroSliderV10 script
v10_script = """
    function heroSliderV10() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Estruturação',
                    title: 'Totem<br/>Triedro.',
                    description: 'Engajamento 360 Graus. Um totem de 3 faces desenvolvido para capturar a atenção de clientes vindos de todas as direções.',
                    image: "{% static 'img/totem_triedro.png' %}?v=16",
                    cta: 'Personalizar',
                    link: '/produto/totem-triedro-em-poliondas/',
                    colorClass: 'bg-blue-300'
                },
                {
                    subtitle: 'Impacto Global',
                    title: 'Cubo<br/>Promo.',
                    description: 'Construa verdadeiros muros criativos em segundos. Caixas robustas para criação de ilhas imponentes.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=10",
                    cta: 'Montar Ilha',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    colorClass: 'bg-orange-300'
                },
                {
                    subtitle: 'Eventos & PDV',
                    title: 'Banner<br/>Rollup.',
                    description: 'O parceiro ideal para eventos inesquecíveis. Extremamente sofisticado e montado num piscar de olhos.',
                    image: "{% static 'img/rollup_hero.png' %}?v=8",
                    cta: 'Configurar',
                    link: '/produto/banner-rollup/',
                    colorClass: 'bg-purple-300'
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
content = content.replace("</script>", v10_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V10 HERO Neo-Bento Grid successfully!")
