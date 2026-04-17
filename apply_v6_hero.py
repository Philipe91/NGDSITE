import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V5 in comments
content = content.replace("<!-- V5 HERO LIGHT MOTION START -->", "{% comment %}\n<!-- V5 HERO LIGHT MOTION START -->")
content = content.replace("<!-- V5 HERO LIGHT MOTION END -->", "<!-- V5 HERO LIGHT MOTION END -->\n{% endcomment %}")

# Prepare V6 (Opção 3 - Centerpiece Depth Illusion)
v6_html = """
<!-- V6 HERO CENTERPIECE DEPTH START -->
<div class="relative w-full min-h-[85vh] lg:h-[95vh] overflow-hidden bg-gray-50 flex items-center justify-center" x-data="heroSliderV6()" x-init="start()" @mousemove="onMouseMove($event)">

    <!-- Background Base with gentle radial focus -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-white via-gray-50 to-gray-200 pointer-events-none z-0"></div>

    <template x-for="(slide, index) in slides" :key="index">
        <div class="absolute inset-0 w-full h-full flex flex-col items-center justify-center"
             x-show="active === index"
             x-transition:enter="transition-opacity duration-1000"
             x-transition:enter-start="opacity-0"
             x-transition:enter-end="opacity-100"
             x-transition:leave="transition-opacity duration-700"
             x-transition:leave-start="opacity-100"
             x-transition:leave-end="opacity-0">

            <!-- MASSIVE BACKGROUND TYPOGRAPHY (Behind the Product) -->
            <div class="absolute inset-0 flex items-center justify-center z-0 overflow-hidden pointer-events-none"
                 :style="`transform: translateX(${mouseX * 20}px)`">
                <h1 class="text-[12rem] md:text-[20rem] lg:text-[28rem] font-black uppercase text-gray-900/[0.03] select-none whitespace-nowrap tracking-tighter"
                    x-show="active === index"
                    x-transition:enter="transition-all duration-[1500ms] ease-out"
                    x-transition:enter-start="opacity-0 scale-90 translate-y-20"
                    x-transition:enter-end="opacity-100 scale-100 translate-y-0"
                    x-text="slide.bigBgText"></h1>
            </div>

            <!-- Foreground Content Container -->
            <div class="container relative z-20 flex flex-col items-center justify-center h-full pt-10">
                
                <!-- Top Section: Badges & Title -->
                <div class="text-center mb-0 relative z-30 pt-10 lg:pt-0"
                     x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-300 ease-out"
                     x-transition:enter-start="opacity-0 -translate-y-10"
                     x-transition:enter-end="opacity-100 translate-y-0">
                    
                    <span class="inline-flex py-1.5 px-4 rounded-full bg-white border border-gray-200 text-gray-800 text-xs font-bold tracking-[0.2em] uppercase mb-6 shadow-sm">
                        <span class="w-1.5 h-1.5 rounded-full bg-primary mr-2 animate-ping inline-block"></span>
                        <span x-text="slide.subtitle"></span>
                    </span>

                    <h2 class="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight leading-none mb-4" x-html="slide.title"></h2>
                    <p class="text-lg text-gray-500 font-medium max-w-lg mx-auto" x-text="slide.description"></p>
                </div>

                <!-- Center Product with Floating Badges -->
                <div class="relative w-full max-w-4xl flex justify-center items-center flex-grow min-h-[45vh] lg:min-h-[55vh] z-20 perspective-1000">
                    <!-- Glow behind image -->
                    <div class="absolute w-[300px] h-[300px] rounded-full blur-[80px] -z-10 transition-colors duration-1000 mix-blend-multiply" :class="slide.glowColor"></div>

                    <!-- Floating Left Badge -->
                    <div class="absolute left-[10%] lg:left-[5%] top-[30%] bg-white/80 backdrop-blur-md px-4 py-3 rounded-2xl shadow-xl shadow-gray-200/50 border border-white z-30 hidden md:flex items-center gap-3 animate-[floating_5s_ease-in-out_infinite]"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-500 delay-[800ms]"
                         x-transition:enter-start="opacity-0 scale-50"
                         x-transition:enter-end="opacity-100 scale-100">
                        <div class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        </div>
                        <div class="text-left">
                            <p class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Qualidade</p>
                            <p class="text-sm font-bold text-gray-800">Premium HD</p>
                        </div>
                    </div>

                    <!-- Floating Right Badge -->
                    <div class="absolute right-[10%] lg:right-[5%] bottom-[20%] bg-white/80 backdrop-blur-md px-4 py-3 rounded-2xl shadow-xl shadow-gray-200/50 border border-white z-30 hidden md:flex items-center gap-3 animate-[floating_6s_ease-in-out_infinite_reverse]"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-500 delay-[900ms]"
                         x-transition:enter-start="opacity-0 scale-50"
                         x-transition:enter-end="opacity-100 scale-100">
                        <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        </div>
                        <div class="text-left">
                            <p class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Produção</p>
                            <p class="text-sm font-bold text-gray-800">Ultra Rápida</p>
                        </div>
                    </div>

                    <!-- The Product Image -->
                    <img :src="slide.image"
                         :alt="slide.title"
                         class="relative w-[120%] lg:w-[130%] max-w-[500px] lg:max-w-[700px] object-contain drop-shadow-[0_40px_40px_rgba(0,0,0,0.15)] transform-gpu transition-transform duration-500 ease-out z-20"
                         :style="`transform: translate3d(${mouseX * -40}px, ${mouseY * -40}px, 0) scale(1.05)`"
                         x-show="active === index"
                         x-transition:enter="transition-all ease-[cubic-bezier(0.34,1.56,0.64,1)] duration-[1200ms] delay-500"
                         x-transition:enter-start="opacity-0 scale-90 translate-y-32"
                         x-transition:enter-end="opacity-100 scale-100 translate-y-0">
                </div>

                <!-- Bottom CTA -->
                <div class="w-full flex justify-center pb-12 lg:pb-8 relative z-30"
                     x-show="active === index"
                     x-transition:enter="transition-all duration-700 delay-1000 ease-out"
                     x-transition:enter-start="opacity-0 translate-y-10"
                     x-transition:enter-end="opacity-100 translate-y-0">
                    <a :href="slide.link" class="group relative px-10 py-5 bg-primary text-white rounded-2xl overflow-hidden shadow-[0_20px_40px_rgba(37,99,235,0.3)] hover:shadow-[0_20px_40px_rgba(37,99,235,0.5)] transition-all duration-300 transform hover:-translate-y-2 inline-flex items-center gap-4">
                        <span class="absolute inset-0 w-full h-full bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                        <span class="relative font-extrabold tracking-[0.1em] uppercase text-sm z-10" x-text="slide.cta"></span>
                        <span class="relative z-10 bg-white/20 p-2 rounded-xl group-hover:bg-white group-hover:text-primary transition-colors">
                            <svg class="w-5 h-5 line-height-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                        </span>
                    </a>
                </div>

            </div>
        </div>
    </template>

    <!-- Side Navigation Points (Vertical dots) -->
    <div class="absolute right-6 top-1/2 -translate-y-1/2 z-40 flex flex-col gap-4">
        <template x-for="(slide, idx) in slides" :key="idx">
            <button @click="goTo(idx)" 
                    class="w-3 h-3 rounded-full transition-all duration-500 relative"
                    :class="active === idx ? 'bg-primary scale-125' : 'bg-gray-300 hover:bg-gray-400'">
                 <!-- Subtle ring on active -->
                 <div x-show="active === idx" class="absolute inset-[-4px] border border-primary rounded-full animate-ping opacity-25"></div>
            </button>
        </template>
    </div>

    <!-- Minimalist Slide Counter (Left) -->
    <div class="absolute left-8 lg:left-12 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col items-center">
        <span class="text-2xl font-black text-gray-900 align-top leading-none" x-text="'0' + (active + 1)"></span>
        <div class="w-px h-12 bg-gray-300 my-2"></div>
        <span class="text-sm font-bold text-gray-400" x-text="'0' + slides.length"></span>
    </div>

</div>

<style>
@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}
</style>
<!-- V6 HERO CENTERPIECE DEPTH END -->
"""
content = content.replace("<!-- V5 HERO LIGHT MOTION END -->\n{% endcomment %}", "<!-- V5 HERO LIGHT MOTION END -->\n{% endcomment %}\n\n" + v6_html)

# Add heroSliderV6 script
v6_script = """
    function heroSliderV6() {
        return {
            active: 0,
            interval: null,
            mouseX: 0,
            mouseY: 0,
            slides: [
                {
                    subtitle: 'Lançamento',
                    title: 'Totem Triedro',
                    description: 'Engajamento 360 Graus. Um totem de 3 faces focado em visibilidade máxima.',
                    image: "{% static 'img/totem_triedro.png' %}?v=12",
                    cta: 'Personalizar Material',
                    link: '/produto/totem-triedro-em-poliondas/',
                    bigBgText: 'TRIEDRO',
                    glowColor: 'bg-blue-300'
                },
                {
                    subtitle: 'Impacto Global',
                    title: 'Cubo Promocional',
                    description: 'Geometria que atrai os olhos. Caixas robustas para vitrines extravagantes.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=6",
                    cta: 'Descobrir Produto',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    bigBgText: 'VITRINE',
                    glowColor: 'bg-orange-300'
                },
                {
                    subtitle: 'Feiras e Eventos',
                    title: 'Banner Rollup',
                    description: 'O parceiro ideal de eventos. Traga impacto instantâneo para sua marca.',
                    image: "{% static 'img/rollup_hero.png' %}?v=4",
                    cta: 'Configurar Banner',
                    link: '/produto/banner-rollup/',
                    bigBgText: 'ROLLUP',
                    glowColor: 'bg-purple-300'
                }
            ],
            start() {
                this.resetInterval();
            },
            onMouseMove(e) {
                // Parallax calculations
                this.mouseX = (e.clientX / window.innerWidth) - 0.5;
                this.mouseY = (e.clientY / window.innerHeight) - 0.5;
            },
            resetInterval() {
                clearInterval(this.interval);
                this.interval = setInterval(() => {
                    this.active = (this.active + 1) % this.slides.length;
                }, 7000);
            },
            goTo(index) {
                this.active = index;
                this.resetInterval();
            }
        }
    }
"""
content = content.replace("</script>", v6_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V6 HERO Centerpiece Illusion successfully!")
