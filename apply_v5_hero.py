import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V4 in comments
content = content.replace("<!-- V4 HERO PREMIUM MOTION START -->", "{% comment %}\n<!-- V4 HERO PREMIUM MOTION START -->")
content = content.replace("<!-- V4 HERO PREMIUM MOTION END -->", "<!-- V4 HERO PREMIUM MOTION END -->\n{% endcomment %}")

# Prepare V5 (Opção 2 - Light Motion)
v5_html = """
<!-- V5 HERO LIGHT MOTION START -->
<div class="relative w-full h-[75vh] lg:h-[90vh] overflow-hidden bg-[#f4f6f8]" x-data="heroSliderV5()" x-init="start()" @mousemove="onMouseMove($event)">

    <!-- Animated Light Gradient Background (Clean Canvas) -->
    <div class="absolute inset-0 z-0 pointer-events-none opacity-80">
        <div class="absolute top-[-10%] left-[0%] w-[60vw] h-[60vw] rounded-full mix-blend-multiply filter blur-[100px] animate-[pulse_8s_ease-in-out_infinite] transition-colors duration-[3000ms]"
            :class="slides[active].glowTop"></div>
        <div class="absolute bottom-[-10%] right-[0%] w-[50vw] h-[50vw] rounded-full mix-blend-multiply filter blur-[120px] animate-[pulse_10s_ease-in-out_infinite_reverse] transition-colors duration-[3000ms]"
            :class="slides[active].glowBottom"></div>
    </div>
    
    <!-- Grain/Grid Overlay for subtle depth -->
    <div class="absolute inset-0 z-[1] pointer-events-none opacity-[0.05]" style="background-image: radial-gradient(#000 1px, transparent 1px); background-size: 24px 24px;"></div>

    <div class="absolute inset-0 w-full h-full z-10 flex">
        <template x-for="(slide, index) in slides" :key="index">
            <div class="absolute inset-0 w-full h-full flex items-center justify-center pt-10"
                 x-show="active === index"
                 x-transition:enter="transition-all ease-[cubic-bezier(0.25,1,0.5,1)] duration-1000"
                 x-transition:enter-start="opacity-0 scale-105"
                 x-transition:enter-end="opacity-100 scale-100"
                 x-transition:leave="transition-all ease-in-out duration-700 z-0"
                 x-transition:leave-start="opacity-100"
                 x-transition:leave-end="opacity-0">

                <div class="container mx-auto px-4 lg:px-8 w-full h-full flex flex-col lg:flex-row items-center relative gap-10">
                    
                    <!-- Left Text Content -->
                    <div class="lg:w-1/2 flex flex-col justify-center relative z-20 text-gray-900 mt-12 lg:mt-0">
                        <!-- Subtitle (Eyebrow text) with tracking -->
                        <div class="overflow-hidden mb-6 flex items-center gap-3">
                            <span class="w-8 h-[3px] bg-primary rounded-full shadow-[0_0_10px_rgba(37,99,235,0.4)]"
                                x-show="active === index"
                                x-transition:enter="transition-all duration-700 delay-300"
                                x-transition:enter-start="opacity-0 -translate-x-full"
                                x-transition:enter-end="opacity-100 translate-x-0"></span>
                            <span class="uppercase tracking-[0.25em] text-sm md:text-[13px] font-extrabold text-primary"
                                x-text="slide.subtitle"
                                x-show="active === index"
                                x-transition:enter="transition-all duration-700 delay-400"
                                x-transition:enter-start="opacity-0 translate-y-full"
                                x-transition:enter-end="opacity-100 translate-y-0"></span>
                        </div>

                        <!-- Main Title -->
                        <div class="mb-8">
                            <h2 class="text-6xl md:text-7xl lg:text-8xl font-black leading-[1.05] tracking-tighter text-gray-900"
                                x-show="active === index"
                                x-transition:enter="transition-all duration-[900ms] delay-500 ease-out"
                                x-transition:enter-start="opacity-0 translate-y-[50px] rotate-2"
                                x-transition:enter-end="opacity-100 translate-y-0 rotate-0"
                                x-html="slide.title"></h2>
                        </div>

                        <!-- Description Box -->
                        <div class="mb-10 w-full max-w-lg"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-700 ease-out"
                             x-transition:enter-start="opacity-0 translate-y-8"
                             x-transition:enter-end="opacity-100 translate-y-0">
                            <p class="text-lg md:text-xl text-gray-600 leading-relaxed font-medium" x-text="slide.description"></p>
                        </div>

                        <!-- Action Buttons -->
                        <div class="flex items-center gap-6"
                             x-show="active === index"
                             x-transition:enter="transition-all duration-700 delay-900 ease-out"
                             x-transition:enter-start="opacity-0 translate-y-8"
                             x-transition:enter-end="opacity-100 translate-y-0">
                            <a :href="slide.link" class="group relative px-8 py-4 bg-gray-900 text-white rounded-full overflow-hidden shadow-xl shadow-gray-900/20 hover:shadow-gray-900/40 transition-all duration-300 transform hover:-translate-y-1 inline-flex items-center gap-3">
                                <span class="absolute inset-0 w-full h-full bg-gradient-to-r from-primary to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                                <span class="relative font-bold tracking-widest uppercase text-xs z-10" x-text="slide.cta"></span>
                                <svg class="w-4 h-4 transform group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                            </a>
                        </div>
                    </div>

                    <!-- Right Image Content with Parallax Hover -->
                    <div class="lg:w-1/2 relative z-20 flex justify-center items-center h-[40vh] lg:h-full perspective-1000">
                        <!-- Shadow floor -->
                        <div class="absolute bottom-[10%] w-[60%] h-[20px] bg-black/20 blur-xl rounded-[100%] transform scale-y-50"></div>
                        
                        <img :src="slide.image"
                             :alt="slide.title"
                             class="relative w-[110%] max-w-2xl object-contain drop-shadow-2xl transform-gpu transition-transform duration-700 ease-out z-10"
                             :style="`transform: translate3d(${mouseX * -30}px, ${mouseY * -30}px, 0) rotateX(${mouseY * 10}deg) rotateY(${mouseX * -10}deg)`"
                             x-show="active === index"
                             x-transition:enter="transition-all ease-[cubic-bezier(0.34,1.56,0.64,1)] duration-[1200ms] delay-500"
                             x-transition:enter-start="opacity-0 scale-75 translate-x-20 rotate-[10deg]"
                             x-transition:enter-end="opacity-100 scale-100 translate-x-0 rotate-0">
                    </div>

                </div>
            </div>
        </template>
    </div>

    <!-- Minimalist Global Progress Bar Bottom Edge -->
    <div class="absolute bottom-0 left-0 h-[4px] bg-gray-200 w-full z-40">
        <div class="h-full bg-primary relative transition-all duration-75"
             :style="`width: ${progress}%`">
            <div class="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 bg-white shadow-xl rounded-full border border-gray-100"></div>     
        </div>
    </div>

    <!-- Floating Navigation & Numbers (Dark Version) -->
    <div class="absolute right-8 top-1/2 -translate-y-1/2 z-40 hidden lg:flex flex-col items-center gap-6">
        <template x-for="(slide, idx) in slides" :key="idx">
            <div class="relative flex items-center justify-center group cursor-pointer" @click="goTo(idx)">
                <span class="absolute right-8 text-xs font-bold text-gray-400 opacity-0 group-hover:opacity-100 group-hover:-translate-x-2 transition-all duration-300" 
                      x-text="'0' + (idx + 1)"></span>
                <div class="w-1.5 rounded-full transition-all duration-500 border border-gray-300"
                     :class="active === idx ? 'h-12 bg-gray-900 border-gray-900' : 'h-3 bg-white hover:bg-gray-400 hover:h-6'"></div>
            </div>
        </template>
    </div>

    <!-- Socials / Small Text Left -->
    <div class="absolute left-8 bottom-12 z-30 hidden md:block">
        <p class="text-gray-400 font-bold text-[10px] tracking-[0.4em] uppercase -rotate-90 origin-left translate-y-[200px]">Produção &bull; Premium &bull; PDV</p>
    </div>
</div>
<!-- V5 HERO LIGHT MOTION END -->
"""
content = content.replace("<!-- V4 HERO PREMIUM MOTION END -->\n{% endcomment %}", "<!-- V4 HERO PREMIUM MOTION END -->\n{% endcomment %}\n\n" + v5_html)

# Add heroSliderV5 script
v5_script = """
    function heroSliderV5() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            mouseX: 0,
            mouseY: 0,
            slides: [
                {
                    subtitle: 'Lançamento',
                    title: 'Totem<br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-500">Triedro</span>',
                    description: 'Engajamento 360 Graus. Um totem de 3 faces desenvolvido para garantir máxima visibilidade em grandes corredores e espaços abertos.',
                    image: "{% static 'img/totem_triedro.png' %}?v=11",
                    cta: 'Personalizar',
                    link: '/produto/totem-triedro-em-poliondas/',
                    glowTop: 'bg-blue-100/80',
                    glowBottom: 'bg-indigo-100/80'
                },
                {
                    subtitle: 'Impacto Global',
                    title: 'Cubo<br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-red-500">Promocional</span>',
                    description: 'Geometria que atrai os olhos. Caixas robustas e leves, excelentes para vitrines extravagantes e empilhamento criativo.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=5",
                    cta: 'Descobrir Cubo',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    glowTop: 'bg-orange-100/80',
                    glowBottom: 'bg-red-100/80'
                },
                {
                    subtitle: 'Elegância e Mobilidade',
                    title: 'Banner<br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-500">Rollup</span>',
                    description: 'O parceiro ideal de eventos premium. Montagem que leva menos de um minuto e um acabamento que valoriza sua marca instantaneamente.',
                    image: "{% static 'img/rollup_hero.png' %}?v=3",
                    cta: 'Configurar',
                    link: '/produto/banner-rollup/',
                    glowTop: 'bg-purple-100/80',
                    glowBottom: 'bg-pink-100/80'
                }
            ],
            start() {
                this.resetInterval();
            },
            onMouseMove(e) {
                // Parallax calculations - from -0.5 to 0.5
                this.mouseX = (e.clientX / window.innerWidth) - 0.5;
                this.mouseY = (e.clientY / window.innerHeight) - 0.5;
            },
            resetInterval() {
                clearInterval(this.interval);
                clearInterval(this.progressInterval);
                this.progress = 0;

                // 8000ms duration per slide
                this.progressInterval = setInterval(() => {
                    this.progress += (100 / (8000 / 16)); // 16ms roughly 60fps
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
content = content.replace("</script>", v5_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V5 HERO Light Motion successfully!")
