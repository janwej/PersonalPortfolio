from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background: linear-gradient(135deg, #4a4a5e 0%, #46516e 25%, #4e5a79 50%, #4a4a5e 75%, #46516e 100%);
            background-attachment: fixed;
            min-height: 100vh;
        }
        
        .glass-card {
            background: rgba(39, 39, 42, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Mobile optimizations */
        @media (max-width: 640px) {
            .page-content {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            
            .glass-card {
                padding: 1.25rem !important;
            }
            
            h1 {
                font-size: 1.875rem !important;
                line-height: 2.25rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
                line-height: 2rem !important;
            }
            
            h3 {
                font-size: 1.25rem !important;
                line-height: 1.75rem !important;
            }
        }
        
        .sidebar {
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .sidebar-open {
            transform: translateX(0);
        }
        
        .sidebar-closed {
            transform: translateX(-100%);
        }
        
        .card-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card-hover:hover {
            transform: translateY(-4px);
        }
        
        .nav-pill {
            transition: all 0.2s ease;
        }
        
        .nav-pill.active {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
        }
        
        .menu-item {
            transition: all 0.2s ease;
        }
        
        .menu-item:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(4px);
        }
        
        .menu-item.active {
            background: rgba(139, 92, 246, 0.1);
            border-left: 3px solid rgb(139, 92, 246);
        }
        
        .page-content {
            display: none;
        }
        
        .page-content.active {
            display: block;
        }
        
        section {
            scroll-margin-top: 100px;
        }

        /* Mobile readability */
        pre {
            white-space: pre-wrap;
            word-break: break-word;
        }
        code {
            white-space: inherit;
        }

        /* Mobile tweaks */
        @media (max-width: 768px) {
            body {
                font-size: 14px;
            }
            h1, h2, h3 {
                line-height: 1.2;
            }
            .text-6xl { font-size: 2rem !important; }
            .text-7xl { font-size: 2.5rem !important; }
            .text-5xl { font-size: 1.75rem !important; }
            .text-4xl { font-size: 1.5rem !important; }
            .text-3xl { font-size: 1.25rem !important; }
            .text-2xl { font-size: 1.15rem !important; }
            .text-xl { font-size: 1.05rem !important; }
            .text-lg { font-size: 0.95rem !important; }
            .text-base { font-size: 0.9rem !important; }
            .pt-32 { padding-top: 5rem !important; }
            .pb-20 { padding-bottom: 3rem !important; }
            .p-8 { padding: 1rem !important; }
            .p-6 { padding: 0.875rem !important; }
            .px-6 { padding-left: 1rem !important; padding-right: 1rem !important; }
            .py-4 { padding-top: 0.75rem !important; padding-bottom: 0.75rem !important; }
            .space-y-12 > * + * { margin-top: 2rem !important; }
            .space-y-8 > * + * { margin-top: 1.5rem !important; }
            .mb-12 { margin-bottom: 1.5rem !important; }
            .mb-8 { margin-bottom: 1.25rem !important; }
            .mb-6 { margin-bottom: 1rem !important; }
            .mb-4 { margin-bottom: 0.75rem !important; }
            #home-nav {
                display: none !important;
            }
            #home-nav::-webkit-scrollbar {
                display: none;
            }
        }
    </style>
</head>
<body class="text-white">
    
    <!-- Sidebar -->
    <div id="sidebar" class="sidebar sidebar-closed fixed top-0 left-0 h-full w-64 glass-card border-r border-zinc-800/50 z-50">
        <div class="p-6">
            <div class="flex items-center justify-between mb-8">
                <h2 class="text-xl font-bold">Menu</h2>
                <button onclick="toggleSidebar()" class="p-2 hover:bg-zinc-800 rounded-lg transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <nav class="space-y-2">
                <button onclick="showPage('home')" class="menu-item active w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left" data-page="home">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
                    </svg>
                    <span class="font-medium">Home</span>
                </button>
                
                <button onclick="showPage('projects')" class="menu-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left text-gray-400" data-page="projects">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                    <span class="font-medium">Projects</span>
                </button>
                
                <button onclick="showPage('academic-works')" class="menu-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left text-gray-400" data-page="academic-works">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    <span class="font-medium">Academic Works</span>
                </button>
                
                <button onclick="showPage('experience')" class="menu-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left text-gray-400" data-page="experience">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    <span class="font-medium">Experience</span>
                </button>
                
                <button onclick="showPage('resume')" class="menu-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left text-gray-400" data-page="resume">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <span class="font-medium">Resume</span>
                </button>
            </nav>
            
            <div class="absolute bottom-6 left-6 right-6">
                <div class="p-4 bg-violet-500/10 rounded-xl border border-violet-500/20">
                    <p class="text-sm text-violet-300 mb-2">💡 Available for work</p>
                    <p class="text-xs text-gray-400">Open to new opportunities</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Overlay -->
    <div id="overlay" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 hidden" onclick="toggleSidebar()"></div>
    
    <!-- Main Content -->
    <div class="min-h-screen">
        <!-- Top Navigation -->
        <nav class="fixed top-0 left-0 right-0 z-30 glass-card border-b border-zinc-800/50">
            <div class="max-w-5xl mx-auto px-4 md:px-6 py-2 md:py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2 md:gap-4">
                        <button onclick="toggleSidebar()" class="p-2 hover:bg-zinc-800/50 rounded-lg transition-colors">
                            <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                        <span class="text-lg md:text-xl font-bold">Portfolio</span>
                    </div>
                    <div id="home-nav" class="hidden md:flex items-center gap-2 bg-zinc-900/50 rounded-full p-1.5">
                        <button onclick="scrollToSection('about')" class="nav-pill active px-5 py-2 rounded-full text-sm font-medium">
                            About
                        </button>
                        <button onclick="scrollToSection('skills')" class="nav-pill px-5 py-2 rounded-full text-sm font-medium text-gray-400">
                            Skills
                        </button>
                        <button onclick="scrollToSection('education')" class="nav-pill px-5 py-2 rounded-full text-sm font-medium text-gray-400">
                            Education
                        </button>
                        <button onclick="scrollToSection('contact')" class="nav-pill px-5 py-2 rounded-full text-sm font-medium text-gray-400">
                            Contact
                        </button>
                    </div>
                    <button id="back-home-btn" onclick="showPage('home')" class="hidden items-center gap-2 px-4 md:px-5 py-2 bg-zinc-900/50 rounded-full text-sm font-medium hover:bg-zinc-800/50 transition-colors">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                        </svg>
                        <span class="hidden lg:inline">Back to Home</span>
                    </button>
                </div>
            </div>
        </nav>

        <!-- Home Page -->
        <div id="page-home" class="page-content active">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-5xl mx-auto space-y-12">
                    
                    <!-- About Section -->
                    <section id="about" class="pb-20">
                        <div class="space-y-8">
                            <div>
                                <div class="inline-block px-4 py-1.5 bg-zinc-800/50 rounded-full text-sm font-medium text-gray-300 mb-6">
                                    Welcome 👋
                                </div>
                                <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
                                    <span class="text-white">Jan Jacek</span> <span class="text-gray-300">Wejchert</span>
                                </h1>
                                <div class="space-y-3 mb-6">
                                    <p class="text-xl md:text-3xl font-semibold text-gray-200">
                                        MSc Business Analytics & Data Science Student
                                    </p>
                                    <p class="text-lg md:text-xl text-gray-400 leading-relaxed">
                                        Working at the intersection of data, analytics, and software
                                    </p>
                                </div>
                                <div class="flex flex-wrap items-center gap-4 md:gap-6 text-base md:text-lg text-gray-400">
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        </svg>
                                        <span>Madrid, Spain</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                        </svg>
                                        <span>Open to opportunities in Europe</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                                <h2 class="text-xl md:text-2xl font-bold mb-4">About Me</h2>
                                <div class="text-gray-300 text-sm md:text-lg leading-relaxed">
                                    <div id="about-preview">
                                        <p class="mb-4">
                                I am an ambitious student raised in Warsaw, Poland, with a long-standing passion for mathematics and analytical thinking. From an early stage, mathematics stood out to me as the most fundamental discipline for understanding the world around us, which led me to pursue Mathematics and Further Mathematics at A-level. I strongly believe that mathematical thinking provides one of the most solid foundations for problem-solving across any field.
                                        </p>
                                        <p class="mb-4">
                                Alongside mathematics, I began exploring coding through summer schools, where I was first exposed to the creative and logical aspects of programming. This early experience sparked a growing interest that would later become a central part of my academic and professional direction.
                                        </p>
                                    </div>
                                    <div id="about-full" class="hidden">
                                        <p class="mb-4">
                                            I am an ambitious student raised in Warsaw, Poland, with a long-standing passion for mathematics and analytical thinking. From an early stage, mathematics stood out to me as the most fundamental discipline for understanding the world around us, which led me to pursue Mathematics and Further Mathematics at A-level. I strongly believe that mathematical thinking provides one of the most solid foundations for problem-solving across any field.
                                        </p>
                                        <p class="mb-4">
                                            Alongside mathematics, I began exploring coding through summer schools, where I was first exposed to the creative and logical aspects of programming. This early experience sparked a growing interest that would later become a central part of my academic and professional direction.
                                        </p>
                                        <p class="mb-4">
                                To build a broad and rigorous foundation, I chose to pursue an undergraduate degree in Economics at the University of St Andrews. I viewed economics as a strong baseline discipline - one that combines quantitative reasoning with real-world decision-making and general business knowledge. During my time at St Andrews, I continued to deepen my mathematical background by taking multiple mathematics modules in my first and second years, while also exploring other areas such as philosophy, which helped me develop critical and abstract thinking.
                                        </p>
                                        <p class="mb-4">
                                It was during university that coding truly captured my attention. Through coursework and projects, I found myself genuinely enjoying spending hours working through programming challenges and building solutions - a clear signal that this was an area I wanted to pursue more seriously.
                                        </p>
                                        <p class="mb-4">
                                            At that point, I set out to find a path that combined my three core interests: mathematics, economics, and programming. This led me to pursue a Master's degree in Business Analytics and Data Science - a decision that has proven to be exactly the right one. I am currently completing this degree, and I find the work both challenging and deeply engaging. For the first time, I feel I have a clear and coherent direction for my foreseeable future.
                                        </p>
                                        <p class="mb-4">
                                Through this program, I am developing strong skills in coding, data analysis, and modern data architectures, and I am highly motivated to continue expanding this knowledge. I am excited to find an opportunity where I can apply these skills in practice, contribute meaningfully, and demonstrate the value I can bring in a professional setting.
                                        </p>
                                        <p class="mb-4">
                                Outside of academics and technology, sport plays a central role in my life. It is essential to my mental well-being and one of my favourite ways to connect with others through shared passion and competition. While studying at St Andrews, I was fortunate to have access to the Old Course, allowing me to play golf regularly, and I was also part of a competitive tennis team representing the university against other institutions across Scotland - an experience I found both rewarding and formative.
                                        </p>
                                        <p class="mb-4">
                                Overall, I consider myself a highly motivated and compassionate individual. When I discover something that genuinely interests me, I commit to it fully and with intensity. I work well in collaborative environments, value teamwork, and always aim to contribute meaningfully to group efforts.
                                </p>
                                    </div>
                                    <button id="about-read-more-btn" onclick="toggleAboutMe()" class="mt-4 text-violet-400 hover:text-violet-300 font-medium flex items-center gap-2 transition-colors">
                                        <span>Read more</span>
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Skills Section -->
                    <section id="skills" class="pb-20">
                        <div class="space-y-8">
                            <div>
                                <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Technical Skills</h2>
                                <p class="text-gray-400 text-lg">Technologies and tools I work with</p>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover">
                                    <div class="flex items-center gap-3 mb-4">
                                        <div class="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">Programming & Analytical Languages</h3>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Python</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">SQL</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">R (RStudio</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Stata</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Mathematica</span>
                                    </div>
                                </div>
                                
                                <div class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover">
                                    <div class="flex items-center gap-3 mb-4">
                                        <div class="w-12 h-12 bg-green-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">Tools & Environments</h3>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Jupyter Notebokk</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">PyCharm</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">GitHub</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">VS Code</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">RStudio</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">SQL development environments</span>
                                    </div>
                                </div>
                                
                                <div class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover">
                                    <div class="flex items-center gap-3 mb-4">
                                        <div class="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">Databases & Storage</h3>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Relational databases (DB2, MySQL)</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">MongoDB</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">HDFS & object storage (S3)</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Data lakes</span>
                                    </div>
                                </div>
                                
                                <div class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover">
                                    <div class="flex items-center gap-3 mb-4">
                                        <div class="w-12 h-12 bg-orange-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">Data Analysis & Modeling</h3>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Data cleaning & preparation</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Exploratory data analysis</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Time series analysis</span>
                                        <span class="px-3 py-1.5 bg-zinc-800/50 rounded-full text-sm text-gray-300">Forecasting</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Education Section -->
                    <section id="education" class="pb-20">
                        <div class="space-y-8">
                            <div>
                                <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Education</h2>
                                <p class="text-gray-400 text-lg">My academic background</p>
                            </div>
                            
                            <div class="space-y-4">
                                <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                                    <div class="flex items-start justify-between flex-wrap gap-4">
                                        <div class="flex gap-4">
                                            <div class="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center flex-shrink-0">
                                                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                                                </svg>
                                            </div>
                                            <div>
                                                <h3 class="text-xl font-bold mb-1">Master of Science in Business Analytics and Data Science</h3>
                                                <p class="text-gray-300 mb-2">IE School of Science and Technology, Madrid, Spain</p>
                                                <p class="text-sm text-gray-400">Running GPA: 3,92 out of 4</p>
                                            </div>
                                        </div>
                                        <div class="px-4 py-2 bg-zinc-800/50 rounded-xl text-sm text-gray-300">
                                            2025 - 2026
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                                    <div class="flex items-start justify-between flex-wrap gap-4">
                                        <div class="flex gap-4">
                                            <div class="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center flex-shrink-0">
                                                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                                                </svg>
                                            </div>
                                            <div>
                                                <h3 class="text-xl font-bold mb-1">Bachelor of Science in Economics</h3>
                                                <p class="text-gray-300 mb-2">University of St Andrews, St Andrews, Scotland</p>
                                                <p class="text-sm text-gray-400">Graduated with Honours of the Second Class (Division l)</p>
                                            </div>
                                        </div>
                                        <div class="px-4 py-2 bg-zinc-800/50 rounded-xl text-sm text-gray-300">
                                            2021 - 2025
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                                    <div class="flex items-start justify-between flex-wrap gap-4">
                                        <div class="flex gap-4">
                                            <div class="w-12 h-12 bg-orange-500/10 rounded-2xl flex items-center justify-center flex-shrink-0">
                                                <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                                                </svg>
                                            </div>
                                            <div>
                                                <h3 class="text-xl font-bold mb-1">International A Levels</h3>
                                                <p class="text-gray-300 mb-2">Akademeia High School, Warsaw, Poland</p>
                                                <p class="text-sm text-gray-400">Economics, Mathematics, Further Mathematics, Polish (A*, A*, A*, A)</p>
                                            </div>
                                        </div>
                                        <div class="px-4 py-2 bg-zinc-800/50 rounded-xl text-sm text-gray-300">
                                            2019 - 2021
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Contact Section -->
                    <section id="contact" class="pb-20">
                        <div class="space-y-8">
                            <div>
                                <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Get In Touch</h2>
                                <p class="text-gray-400 text-lg">Let's connect and create something amazing together</p>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <a href="mailto:jan.wejchert@student.ie.edu" class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover block">
                                    <div class="flex items-center gap-4 mb-3">
                                        <div class="w-12 h-12 bg-blue-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">Email</h3>
                                    </div>
                                    <p class="text-gray-300">jan.wejchert@student.ie.edu</p>
                                </a>
                                
                                <a href="https://github.com/janwej" target="_blank" class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover block">
                                    <div class="flex items-center gap-4 mb-3">
                                        <div class="w-12 h-12 bg-purple-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-purple-400" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">GitHub</h3>
                                    </div>
                                    <p class="text-gray-300">github.com/janwej</p>
                                </a>
                                
                                <a href="https://linkedin.com/in/jan-wejchert" target="_blank" class="glass-card rounded-3xl p-6 border border-zinc-800/50 card-hover block">
                                    <div class="flex items-center gap-4 mb-3">
                                        <div class="w-12 h-12 bg-green-500/10 rounded-2xl flex items-center justify-center">
                                            <svg class="w-6 h-6 text-green-400" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                                            </svg>
                                        </div>
                                        <h3 class="text-xl font-bold">LinkedIn</h3>
                                    </div>
                                    <p class="text-gray-300">linkedin.com/in/jan-wejchert</p>
                                </a>
                            </div>
                        </div>
                    </section>

                </div>
            </div>
        </div>

        <!-- Projects Page -->
        <div id="page-projects" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-5xl mx-auto">
                    <div class="mb-12">
                        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Projects</h1>
                        <p class="text-gray-400 text-lg">A showcase of my recent work and side projects</p>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                            </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-blue-500/10 text-blue-400 rounded-full text-xs font-medium mb-3">
                                    Data Analysis
                                </div>
                                <h3 class="text-2xl font-bold mb-2">F1 Data Project</h3>
                                <p class="text-gray-400 mb-4">Fun project conducted for python class to play with f1 data set and to come up with some story from the given data</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Comeback King</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Decade Champions</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Who will come out on top</span>
                                </div>
                                <button onclick="showPage('f1-project')" class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Project</button>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                </svg>
                            </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-cyan-500/10 text-cyan-400 rounded-full text-xs font-medium mb-3">
                                    Time Series
                                </div>
                                <h3 class="text-2xl font-bold mb-2">Time Series & Forecasting Project</h3>
                                <p class="text-gray-400 mb-4">Applied time series analysis using real-world data to explore trends, seasonality, and forecasting performance. Implemented and evaluated classical forecasting methods including moving averages and exponential smoothing.</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Python</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Time Series Analysis</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Forecasting</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Data Visualization</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Model Evaluation</span>
                                </div>
                                <button onclick="showPage('timeseries-project')" class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Details</button>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
                                </svg>
                            </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-yellow-500/10 text-yellow-400 rounded-full text-xs font-medium mb-3">
                                    Big Data
                                </div>
                                <h3 class="text-2xl font-bold mb-2">Apache Spark DataFrames Project</h3>
                                <p class="text-gray-400 mb-4">Group project using Apache Spark's DataFrames and SQL APIs to perform large-scale data processing and exploratory analysis. Focused on distributed computation, transformations, joins, and aggregations.</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Apache Spark</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Spark SQL</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Distributed Processing</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Big Data Analytics</span>
                                </div>
                                <button class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Details</button>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path>
                                </svg>
                            </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-indigo-500/10 text-indigo-400 rounded-full text-xs font-medium mb-3">
                                    Data Pipeline
                                </div>
                                <h3 class="text-2xl font-bold mb-2">Earthquake Data Pipeline (NiFi + MinIO)</h3>
                                <p class="text-gray-400 mb-4">Designed and implemented an automated data ingestion pipeline that retrieves live earthquake data from the USGS API, processes it using Apache NiFi, and stores structured outputs in an S3-compatible object store (MinIO).</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Apache NiFi</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Data Ingestion</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">MinIO / S3</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">JSON & CSV</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Batch Scheduling</span>
                                </div>
                                <button class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Details</button>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                </svg>
                    </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-xs font-medium mb-3">
                                    Economic Modeling
                </div>
                                <h3 class="text-2xl font-bold mb-2">Solving a Growth Model Using Shooting and Genetic Algorithms</h3>
                                <p class="text-gray-400 mb-4">Solves a deterministic neoclassical growth model using two numerical approaches: shooting algorithm and genetic algorithm. Compares convergence, stability, and behavior of classical optimization methods versus evolutionary algorithms.</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Mathematica</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Shooting Algorithm</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Genetic Algorithm</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Economic Modeling</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Numerical Optimization</span>
                                </div>
                                <button onclick="showPage('growth-model-project')" class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Details</button>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col">
                            <div class="h-40 md:h-48 bg-gradient-to-br from-pink-500/20 to-rose-500/20 flex items-center justify-center">
                                <svg class="w-16 h-16 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
                                </svg>
                            </div>
                            <div class="p-4 md:p-6 flex flex-col h-full">
                                <div class="inline-block px-3 py-1 bg-pink-500/10 text-pink-400 rounded-full text-xs font-medium mb-3">
                                    Optimization
                                </div>
                                <h3 class="text-2xl font-bold mb-2">Graph Optimization with Dynamic Programming</h3>
                                <p class="text-gray-400 mb-4">Complete shortest-path solver in Mathematica using dynamic programming and Bellman iteration. Constructs distance matrices, computes optimal cost-to-go functions, and recovers optimal paths with minimum total cost.</p>
                                <div class="flex flex-wrap gap-2 mb-4">
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Mathematica</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Dynamic Programming</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Bellman Iteration</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Graph Optimization</span>
                                    <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Shortest Path</span>
                                </div>
                                <button onclick="showPage('graph-optimization-project')" class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors mt-auto">View Details</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Experience Page -->
        <div id="page-experience" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-5xl mx-auto">
                    <div class="mb-12">
                        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Experience</h1>
                        <p class="text-gray-400 text-lg">My professional journey</p>
                    </div>
                    
                    <div class="space-y-6">
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                            <div class="flex items-start justify-between flex-wrap gap-4 mb-4">
                                <div>
                                    <h3 class="text-2xl font-bold mb-2">Brevan Howard Intern</h3>
                                    <p class="text-violet-400 font-medium mb-2">Global Macro Hedge Fund</p>
                                    <p class="text-sm text-gray-400">Intern at Brevan Howard, gaining hands-on exposure to global macro trading, portfolio construction, and risk frameworks while supporting portfolio managers with analytical tools and proprietary financial modeling.</p>
                                </div>
                                <div class="px-4 py-2 bg-zinc-800/50 rounded-xl text-sm text-gray-300">
                                    2024 Summer
                                </div>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">London</span>
                                <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">Abu Dhabi</span>
                            </div>
                        </div>
                        
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 card-hover">
                            <div class="flex items-start justify-between flex-wrap gap-4 mb-4">
                                <div>
                                    <h3 class="text-2xl font-bold mb-2">Passion Capital Intern</h3>
                                    <p class="text-violet-400 font-medium mb-2">Early-stage venture capital firm</p>
                                    <p class="text-sm text-gray-400">Intern at Passion Capital, contributing to early-stage venture capital sourcing and due diligence through startup analysis, founder meetings, and investment research across AI and fintech.</p>
                                </div>
                                <div class="px-4 py-2 bg-zinc-800/50 rounded-xl text-sm text-gray-300">
                                    2023 Summer
                                </div>
                            </div>
                            <div class="flex flex-wrap gap-2">
                                <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">London</span>
                            </div>
                        </div>
                        
                                </div>
                </div>
            </div>
        </div>

        <!-- Resume Page -->
        <div id="page-resume" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-5xl mx-auto">
                    <div class="mb-12 flex items-center justify-between flex-wrap gap-4">
                        <div>
                            <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Resume</h1>
                            <p class="text-gray-400 text-lg">Download or view my full resume</p>
                        </div>
                        <a href="/IE_CV.pdf" download class="px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            Download PDF
                        </a>
                    </div>
                    
                    <div class="glass-card rounded-3xl p-12 border border-zinc-800/50">
                        <div class="space-y-8">
                            <div class="text-center">
                                <h2 class="text-3xl sm:text-4xl font-bold mb-2">Jan Jacek Wejchert</h2>
                                <p class="text-xl text-gray-300 mb-4">MSc Business Analytics & Data Science Student</p>
                                <div class="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-400">
                                    <a href="mailto:jan.wejchert@student.ie.edu" class="flex items-center gap-2 hover:text-gray-300 transition-colors">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                        </svg>
                                        <span>jan.wejchert@student.ie.edu</span>
                                    </a>
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        </svg>
                                        <span>Madrid, Spain</span>
                                    </div>
                                    <a href="https://github.com/janwej" target="_blank" class="flex items-center gap-2 hover:text-gray-300 transition-colors">
                                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                                        </svg>
                                        <span>github.com/janwej</span>
                                    </a>
                                    <a href="https://linkedin.com/in/jan-wejchert" target="_blank" class="flex items-center gap-2 hover:text-gray-300 transition-colors">
                                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                                        </svg>
                                        <span>LinkedIn</span>
                                    </a>
                                </div>
                            </div>
                            
                            <div class="border-t border-zinc-800 pt-8">
                                <h3 class="text-2xl font-bold mb-4">Professional Summary</h3>
                                <p class="text-gray-300 leading-relaxed">
                                    Ambitious MSc student in Business Analytics and Data Science with a strong foundation in mathematics, economics, and programming. 
                                    Passionate about working at the intersection of data, analytics, and software to solve complex business problems. 
                                    Currently developing expertise in data analysis, modern data architectures, and coding through rigorous academic coursework. 
                                    Highly motivated to apply analytical thinking and technical skills in a professional setting, with a commitment to continuous learning and collaborative problem-solving.
                                </p>
                            </div>
                            
                            <div class="border-t border-zinc-800 pt-8">
                                <h3 class="text-2xl font-bold mb-6">Education</h3>
                                <div class="space-y-6">
                                    <div>
                                        <div class="flex items-start justify-between flex-wrap gap-4 mb-2">
                                            <div>
                                                <h4 class="text-lg font-semibold text-gray-200">Master of Science in Business Analytics and Data Science</h4>
                                                <p class="text-gray-400">IE School of Science and Technology, Madrid, Spain</p>
                                            </div>
                                            <span class="text-sm text-gray-400">2025 - 2026</span>
                                        </div>
                                        <p class="text-sm text-gray-400">Running GPA: 3.92 out of 4</p>
                                    </div>
                                    
                                    <div>
                                        <div class="flex items-start justify-between flex-wrap gap-4 mb-2">
                                            <div>
                                                <h4 class="text-lg font-semibold text-gray-200">Bachelor of Science in Economics</h4>
                                                <p class="text-gray-400">University of St Andrews, St Andrews, Scotland</p>
                                            </div>
                                            <span class="text-sm text-gray-400">2021 - 2025</span>
                                        </div>
                                        <p class="text-sm text-gray-400">Graduated with Honours of the Second Class (Division I)</p>
                                    </div>
                                    
                                    <div>
                                        <div class="flex items-start justify-between flex-wrap gap-4 mb-2">
                                            <div>
                                                <h4 class="text-lg font-semibold text-gray-200">International A Levels</h4>
                                                <p class="text-gray-400">Akademeia High School, Warsaw, Poland</p>
                                            </div>
                                            <span class="text-sm text-gray-400">2019 - 2021</span>
                                        </div>
                                        <p class="text-sm text-gray-400">Economics, Mathematics, Further Mathematics, Polish (A*, A*, A*, A)</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="border-t border-zinc-800 pt-8">
                                <h3 class="text-2xl font-bold mb-4">Technical Skills</h3>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <h4 class="font-semibold text-gray-300 mb-3">Programming & Analytical Languages</h4>
                                        <p class="text-gray-400 text-sm">Python, SQL, R (RStudio), Stata, Mathematica</p>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-gray-300 mb-3">Tools & Environments</h4>
                                        <p class="text-gray-400 text-sm">Jupyter Notebook, PyCharm, GitHub, VS Code, RStudio, SQL development environments</p>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-gray-300 mb-3">Databases & Storage</h4>
                                        <p class="text-gray-400 text-sm">Relational databases (DB2, MySQL), MongoDB, HDFS & object storage (S3), Data lakes</p>
                                    </div>
                                    <div>
                                        <h4 class="font-semibold text-gray-300 mb-3">Data Analysis & Modeling</h4>
                                        <p class="text-gray-400 text-sm">Data cleaning & preparation, Exploratory data analysis, Time series analysis, Forecasting</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Academic Works Page -->
        <div id="page-academic-works" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-5xl mx-auto">
                    <div class="mb-12">
                        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Academic Works</h1>
                        <p class="text-gray-400 text-lg">A collection of my academic papers, research, and scholarly contributions</p>
                    </div>
                    
                    <div id="academic-works-list" class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
                        <!-- Academic works will be dynamically added here -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Individual Academic Work Page -->
        <div id="page-academic-work" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-6xl mx-auto">
                    <div class="mb-12">
                        <div class="mb-6">
                            <button onclick="showPage('academic-works')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                <span class="font-medium">Back to Academic Works</span>
                            </button>
                        </div>
                        <div class="flex items-start justify-between flex-wrap gap-4 mb-6">
                            <div class="flex-1 min-w-0">
                                <h1 id="academic-work-title" class="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Academic Work Title</h1>
                                <p id="academic-work-subtitle" class="text-gray-400 text-lg">Work subtitle and description</p>
                            </div>
                            <div id="academic-work-download" class="flex gap-3 flex-shrink-0">
                                <!-- Download buttons will be added here dynamically -->
                            </div>
                        </div>
                        
                        <!-- Academic Work Content -->
                        <div id="academic-work-content" class="space-y-8">
                            <!-- Content will be dynamically loaded here -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- F1 Project Page -->
        <div id="page-f1-project" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-6xl mx-auto">
                    <div class="mb-12">
                        <div class="mb-6">
                            <button onclick="showPage('projects')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                <span class="font-medium">Back to Projects</span>
                            </button>
                        </div>
                        <div class="flex flex-col md:flex-row items-start justify-between gap-4 mb-6">
                            <div class="flex-1 min-w-0">
                                <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-2 md:mb-4">The Comeback King: F1's Greatest Position-Gainer</h1>
                                <p class="text-gray-400 text-base md:text-lg">A Python data analysis project exploring F1 driver comeback performance</p>
                            </div>
                            <a href="/The-Comeback-King-F1s-Greatest-Position-Gainer.pdf" download class="px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2 w-full md:w-auto justify-center">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                                Download Presentation
                            </a>
                        </div>
                        
                        <!-- Project Overview -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-4">Project Overview</h2>
                            <p class="text-gray-300 text-lg leading-relaxed mb-4">
                                This project analyzes Formula 1 historical data to identify the greatest "comeback driver" in F1 history - 
                                the driver who gained the most positions during races across their career. Using a multi-category scoring 
                                system and a decade-based knockout competition, we crowned Sebastian Vettel as the ultimate Comeback King.
                            </p>
                            
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-violet-400 font-bold mb-1">Language</div>
                                    <div class="text-gray-300">Python</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-violet-400 font-bold mb-1">Tools</div>
                                    <div class="text-gray-300">Pandas, Jupyter Notebook</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-violet-400 font-bold mb-1">Winner</div>
                                    <div class="text-gray-300">Sebastian Vettel</div>
                                </div>
                            </div>
                        </div>

                        <!-- Methodology -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Methodology</h2>
                            
                            <h3 class="text-xl font-bold mb-3 text-violet-400">Categories for Evaluation:</h3>
                            <div class="space-y-3 mb-6">
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">1.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Average positions gained per race</span>
                                        <span class="text-gray-400"> - includes dropped positions</span>
                                    </div>
                                </div>
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">2.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Total positions gained in all races</span>
                                        <span class="text-gray-400"> - includes dropped positions</span>
                                    </div>
                                </div>
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">3.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Record positions gained within one race</span>
                                    </div>
                                </div>
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">4.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Circuits with highest average positions gained</span>
                                    </div>
                                </div>
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">5.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Circuit records for most positions gained</span>
                                    </div>
                                </div>
                                <div class="flex gap-3">
                                    <span class="text-violet-400 font-bold">6.</span>
                                    <div>
                                        <span class="font-semibold text-gray-200">Comeback Rate</span>
                                        <span class="text-gray-400"> - percentage of races with positive position gain</span>
                                    </div>
                                </div>
                            </div>

                            <h3 class="text-xl font-bold mb-3 text-violet-400">Scoring System:</h3>
                            <p class="text-gray-300 mb-2">In each category, points were awarded to top 3 drivers:</p>
                            <ul class="list-disc list-inside text-gray-300 space-y-1 mb-6">
                                <li>1st place: 3 points</li>
                                <li>2nd place: 2 points</li>
                                <li>3rd place: 1 point</li>
                                <li>Ties: All tied drivers receive points for that position</li>
                            </ul>

                            <h3 class="text-xl font-bold mb-3 text-violet-400">Competition Structure:</h3>
                            <p class="text-gray-300">Drivers were grouped by decade (1950s-2020s), with decade winners advancing through knockout rounds until a final champion was crowned.</p>
                        </div>

                        <!-- Code Section -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Python Code</h2>
                            
                            <div class="space-y-6">
                                <!-- Data Filtering -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">1. Filter drivers with at least 24 races (1 season)</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300">f1new = f1.groupby("driver")[["grid_starting_position"]].count().reset_index()
f1_group = f1new[f1new["grid_starting_position"] >= 24]["driver"]
f1_filtered = f1[f1["driver"].isin(f1_group)]</code></pre>
                                </div>

                                <!-- Calculate Positions Gained -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">2. Calculate positions gained and filter by decade</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300">race_finishers = f1_filtered[~f1_filtered["final_position"].isna()].copy()
race_finishers["positions_gained"] = race_finishers["grid_starting_position"] - race_finishers["final_position"]
race_finishers = race_finishers[(race_finishers["year"] >= 1960) & (race_finishers["year"] < 1970)]</code></pre>
                                </div>

                                <!-- Scoring Setup -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">3. Set up scoring system</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300">from collections import defaultdict

driver_points = defaultdict(int)  # driver -> total points
rank_to_points = {1: 3, 2: 2, 3: 1}</code></pre>
                                </div>

                                <!-- Points Function -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">4. Function to add points from race results</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300">def add_points_from_series(ser, points_dict):
    current_rank = 0
    last_value = object()  # something that can't equal a real value
    for driver, value in ser.items():
        # new distinct value -> new place (1st, 2nd, 3rd, ...)
        if value != last_value:
            current_rank += 1
            last_value = value
        # only 1st/2nd/3rd place get points
        if current_rank > 3:
            break
        points_dict[driver] += rank_to_points[current_rank]</code></pre>
                                </div>

                                <!-- Categories -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">5. Evaluate all categories</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300"># Category 1: Average positions gained per race
s1 = race_finishers.groupby("driver")["positions_gained"].mean().sort_values(ascending=False).head()
add_points_from_series(s1, driver_points)

# Category 2: Total positions gained in all races
s2 = race_finishers.groupby("driver")["positions_gained"].count().sort_values(ascending=False).head()
add_points_from_series(s2, driver_points)

# Category 3: Record positions gained within one race
s3 = race_finishers.groupby("driver")["positions_gained"].max().sort_values(ascending=False)
add_points_from_series(s3, driver_points)

# Category 4: Circuits with highest average positions gained
avg_gains = race_finishers.groupby(["circuit_name", "driver"])["positions_gained"].mean().reset_index()
best_avg = avg_gains.groupby("circuit_name")["positions_gained"].max().reset_index().rename(
    columns={"positions_gained": "max_avg_positions_gained"})
result = avg_gains.merge(best_avg, on="circuit_name")
result = result[result["positions_gained"] == result["max_avg_positions_gained"]]
s4 = result["driver"].value_counts().head(20)
add_points_from_series(s4, driver_points)

# Category 5: Circuit records for most positions gained
max_gains = race_finishers.groupby("circuit_name")["positions_gained"].max().reset_index().rename(
    columns={"positions_gained": "max_positions_gained"})
result = race_finishers.merge(max_gains, on="circuit_name")
result = result[result["positions_gained"] == result["max_positions_gained"]]
s5 = result["driver"].value_counts().head(10)
add_points_from_series(s5, driver_points)

# Category 6: Comeback Rate (percentage of races with positive position gain)
comeback_rate = race_finishers.assign(
    comeback = race_finishers["positions_gained"] > 0
).groupby("driver")["comeback"].mean() * 100
s6 = comeback_rate.sort_values(ascending=False).head(10)
add_points_from_series(s6, driver_points)</code></pre>
                                </div>

                                <!-- Find Winner -->
                                <div>
                                    <h3 class="text-lg font-bold mb-3 text-violet-400">6. Determine decade winner</h3>
                                    <pre class="bg-black/40 rounded-xl p-4 overflow-x-auto"><code class="text-sm text-gray-300">champion = dict(driver_points)
print(champion)

max_value = max(champion.values())
keys_with_max_value = [k for k, v in champion.items() if v == max_value]
print(keys_with_max_value)</code></pre>
                                </div>
                            </div>
                        </div>

                        <!-- Results -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mt-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Competition Results</h2>
                            
                            <div class="space-y-6">
                                <div>
                                    <h3 class="text-xl font-bold mb-3 text-violet-400">Decade Champions</h3>
                                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">1950s</div>
                                            <div class="font-bold">Johnny Claes</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">1960s</div>
                                            <div class="font-bold">Carel Godin de Beaufort</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">1970s</div>
                                            <div class="font-bold">Hector Rebaque</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">1980s</div>
                                            <div class="font-bold">Marc Surer</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">1990s</div>
                                            <div class="font-bold">Alex Caffi</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">2000s</div>
                                            <div class="font-bold">Tarso Marques</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">2010s</div>
                                            <div class="font-bold">Sebastian Vettel</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-lg p-3">
                                            <div class="text-gray-400 text-sm">2020s</div>
                                            <div class="font-bold">Max Verstappen</div>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 class="text-xl font-bold mb-3 text-violet-400">Final Winner</h3>
                                    <div class="bg-gradient-to-r from-violet-500/20 to-purple-500/20 border-2 border-violet-500/50 rounded-xl p-6 text-center">
                                        <div class="text-5xl font-bold mb-2">🏆 Sebastian Vettel 🏆</div>
                                        <div class="text-gray-300 text-lg">The Comeback King</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Time Series Project Page -->
        <div id="page-timeseries-project" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-6xl mx-auto">
                    <div class="mb-12">
                        <div class="mb-6">
                            <button onclick="showPage('projects')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                <span class="font-medium">Back to Projects</span>
                            </button>
                        </div>
                        <div class="flex flex-col md:flex-row items-start justify-between gap-4 mb-6">
                            <div class="flex-1 min-w-0">
                                <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-2 md:mb-4">Time Series Analysis & Forecasting (CO₂ Concentration Data)</h1>
                                <p class="text-gray-400 text-base md:text-lg">An applied time series analysis project exploring trends, seasonality, and forecasting performance</p>
                            </div>
                            <div class="flex flex-col gap-3 flex-shrink-0 w-full md:w-auto">
                                <a href="/Project1_Final.ipynb" download class="px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download Notebook
                                </a>
                                <a href="/co2.json" download class="px-6 py-3 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl font-medium transition-colors flex items-center gap-2">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download Data
                                </a>
                            </div>
                        </div>
                        
                        <!-- Overview -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Overview</h2>
                            <p class="text-gray-300 text-lg leading-relaxed mb-4">
                                This project focuses on the analysis and forecasting of atmospheric CO₂ concentration levels using historical time series data. The objective was to identify long-term trends and seasonal patterns in the data, and to evaluate the performance of classical forecasting methods on a real-world environmental dataset.
                            </p>
                        </div>

                        <!-- Data & Context -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Data & Context</h2>
                            <p class="text-gray-300 leading-relaxed">
                                The analysis uses monthly CO₂ concentration data, covering several decades, allowing for clear observation of both long-term upward trends and recurring seasonal fluctuations. The dataset was cleaned, structured, and indexed as a time series to enable proper temporal analysis.
                            </p>
                        </div>

                        <!-- Analysis & Methodology -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Analysis & Methodology</h2>
                            <p class="text-gray-300 leading-relaxed mb-6">
                                The project followed a structured time series workflow:
                            </p>
                            <div class="space-y-4">
                                <div class="flex gap-4">
                                    <div class="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                        <span class="text-cyan-400 font-bold">1</span>
                                    </div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-200 mb-2">Exploratory Analysis</h3>
                                        <p class="text-gray-400">Visualization of long-term trends and seasonal behavior</p>
                                    </div>
                                </div>
                                <div class="flex gap-4">
                                    <div class="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                        <span class="text-cyan-400 font-bold">2</span>
                                    </div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-200 mb-2">Time Series Decomposition</h3>
                                        <p class="text-gray-400">Breaking down the series into trend, seasonal, and residual components</p>
                                    </div>
                                </div>
                                <div class="flex gap-4">
                                    <div class="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                        <span class="text-cyan-400 font-bold">3</span>
                                    </div>
                                    <div>
                                        <h3 class="text-lg font-semibold text-gray-200 mb-2">Baseline Smoothing Methods</h3>
                                        <p class="text-gray-400">Implementation of smoothing techniques to reduce noise and capture underlying dynamics</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Forecasting Techniques -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Forecasting Techniques Implemented</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Simple Moving Averages</h3>
                                    <p class="text-gray-300 text-sm">To smooth short-term volatility and identify underlying patterns</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Exponential Smoothing</h3>
                                    <p class="text-gray-300 text-sm">To assign greater weight to recent observations for more responsive forecasts</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Parameter Comparison</h3>
                                    <p class="text-gray-300 text-sm">Comparison of forecasts across different smoothing parameters</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Out-of-Sample Evaluation</h3>
                                    <p class="text-gray-300 text-sm">Using train/test splits to assess predictive accuracy</p>
                                </div>
                            </div>
                        </div>

                        <!-- Key Findings -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Key Findings</h2>
                            <div class="space-y-4">
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Strong Upward Trend & Seasonality</h3>
                                    <p class="text-gray-300">The CO₂ series exhibits a strong, persistent upward trend alongside clear seasonal cycles</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Moving Averages Performance</h3>
                                    <p class="text-gray-300">Moving averages effectively smooth noise but lag during periods of rapid change</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Exponential Smoothing Advantages</h3>
                                    <p class="text-gray-300">Exponential smoothing provides more responsive forecasts and better short-term performance</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-cyan-400 mb-2">Trade-off Analysis</h3>
                                    <p class="text-gray-300">Model choice involves a clear trade-off between stability and adaptability</p>
                                </div>
                            </div>
                        </div>

                        <!-- Tools & Technologies -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Tools & Technologies</h2>
                            <div class="flex flex-wrap gap-3">
                                <span class="px-4 py-2 bg-zinc-800/50 rounded-full text-sm text-gray-300">Python</span>
                                <span class="px-4 py-2 bg-zinc-800/50 rounded-full text-sm text-gray-300">Pandas</span>
                                <span class="px-4 py-2 bg-zinc-800/50 rounded-full text-sm text-gray-300">Time Series Analysis Libraries</span>
                                <span class="px-4 py-2 bg-zinc-800/50 rounded-full text-sm text-gray-300">Data Visualization</span>
                            </div>
                        </div>

                        <!-- Skills Demonstrated -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Skills Demonstrated</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="flex items-center gap-3">
                                    <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Time series structuring and indexing</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Trend and seasonality analysis</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Forecasting and model evaluation</span>
                                </div>
                                <div class="flex items-center gap-3">
                                    <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Analytical interpretation of temporal data</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Graph Optimization Project Page -->
        <div id="page-graph-optimization-project" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-6xl mx-auto">
                    <div class="mb-12">
                        <div class="mb-6">
                            <button onclick="showPage('projects')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                <span class="font-medium">Back to Projects</span>
                            </button>
                        </div>
                        <div class="flex flex-col md:flex-row items-start justify-between gap-4 mb-6">
                            <div class="flex-1 min-w-0">
                                <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-2 md:mb-4">Graph Optimization with Dynamic Programming</h1>
                                <p class="text-gray-400 text-base md:text-lg">A complete shortest-path solver in Mathematica using dynamic programming and Bellman iteration</p>
                            </div>
                            <div class="flex-shrink-0 w-full md:w-auto">
                                <a href="/EC3307Graph.nb" download class="px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download Notebook
                                </a>
                            </div>
                        </div>
                        
                        <!-- Overview -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Overview</h2>
                            <p class="text-gray-300 text-lg leading-relaxed mb-4">
                                In this project, I built a complete shortest-path solver in Mathematica using dynamic programming and Bellman iteration. Starting from raw graph edge data, the workflow constructs a distance matrix, iteratively computes a cost-to-go function, and then recovers the optimal path and its total cost from a chosen start node to the destination.
                            </p>
                            <div class="mt-6 bg-zinc-800/30 rounded-xl p-5">
                                <h3 class="text-lg font-semibold text-pink-400 mb-3">Example Output</h3>
                                <div class="space-y-2 text-gray-300">
                                    <p><strong>Optimal Path:</strong> {17, 23, 33, 41, 53, 56, 57, 60, 67, 70, 73, 76, 85, 89, 99}</p>
                                    <p><strong>Minimum Cost:</strong> 194.22</p>
                                </div>
                            </div>
                        </div>

                        <!-- Problem Statement -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Problem Statement</h2>
                            <p class="text-gray-300 leading-relaxed mb-4">
                                Given a directed weighted graph (nodes + edges + weights), the goal is to:
                            </p>
                            <ol class="list-decimal list-inside space-y-2 text-gray-300 ml-4">
                                <li>Convert the graph representation into a distance matrix <em>Q</em>, assigning Infinity to non-connected node pairs.</li>
                                <li>Use Bellman's operator to compute the optimal cost-to-go <em>J</em> for each node.</li>
                                <li>Use <em>Q</em> and <em>J</em> to reconstruct the cheapest path and its total cost.</li>
                            </ol>
                        </div>

                        <!-- Implementation Details -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Implementation Details</h2>
                            
                            <div class="space-y-8">
                                <!-- Module 1 -->
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-pink-400">1) Data Import & Distance Matrix Construction (dataToMatrix)</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        I implemented a module that reads graph data from a text-based input file, parses each line into (source, destination, weight) connections, and constructs a full distance matrix <em>Q</em> where:
                                    </p>
                                    <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4 mb-4">
                                        <li><em>Q[i, j]</em> = weight if an edge exists</li>
                                        <li><em>Q[i, j]</em> = Infinity if nodes are not connected</li>
                                        <li>The destination node has a diagonal value of 0 to act as the terminal condition</li>
                                    </ul>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <h4 class="text-sm font-semibold text-pink-400 mb-2">Key Features:</h4>
                                        <ul class="text-sm text-gray-300 space-y-1">
                                            <li>• Robust parsing of node identifiers (e.g., stripping the "node" prefix)</li>
                                            <li>• Defensive checks for malformed rows and failed imports</li>
                                            <li>• Correct handling of 1-based indexing in Mathematica while working with 0-based node labels</li>
                                        </ul>
                                    </div>
                                </div>

                                <!-- Module 2 -->
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-pink-400">2) Bellman Operator Update (bellmanIteration)</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        I implemented the Bellman update step as a vector operation over nodes. For each node <em>v</em>, compute:
                                    </p>
                                    <div class="bg-zinc-800/30 rounded-xl p-4 mb-4">
                                        <p class="text-gray-300 font-mono text-sm">
                                            <em>J<sub>n+1</sub>(v)</em> = min<sub>w</sub>(<em>Q(v, w)</em> + <em>J<sub>n</sub>(w)</em>)
                                        </p>
                                    </div>
                                    <p class="text-gray-300 leading-relaxed">
                                        The implementation explicitly handles missing edges by treating Infinity weights as invalid transitions. The output of this step is a new cost-to-go vector.
                                    </p>
                                </div>

                                <!-- Module 3 -->
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-pink-400">3) Convergence to Final Cost-to-Go (findCostToGo)</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        This module repeatedly applies the Bellman operator until convergence:
                                    </p>
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                        <div class="bg-zinc-800/30 rounded-xl p-4">
                                            <div class="text-pink-400 font-bold mb-1">Max Iterations</div>
                                            <div class="text-gray-300">500</div>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-xl p-4">
                                            <div class="text-pink-400 font-bold mb-1">Tolerance</div>
                                            <div class="text-gray-300">10<sup>-6</sup></div>
                                        </div>
                                    </div>
                                    <p class="text-gray-300 leading-relaxed">
                                        To avoid instability from unreachable nodes, the convergence check ignores Infinity values when computing the norm difference. The output is the final cost-to-go vector where <em>J[node]</em> represents the minimum cost required to reach the destination node from that node.
                                    </p>
                                </div>

                                <!-- Module 4 -->
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-pink-400">4) Optimal Path Recovery (findPathAndTotalCost)</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        Once <em>Q</em> and <em>J</em> are computed, I reconstruct the optimal path from a chosen start node by repeatedly selecting the next node that minimizes:
                                    </p>
                                    <div class="bg-zinc-800/30 rounded-xl p-4 mb-4">
                                        <p class="text-gray-300 font-mono text-sm">
                                            <em>Q(current, w)</em> + <em>J(w)</em>
                                        </p>
                                    </div>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        This yields the sequence of nodes visited and the total accumulated cost along the path. The module prints:
                                    </p>
                                    <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                                        <li>Optimal Path</li>
                                        <li>Minimum Cost</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Results -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Results</h2>
                            <p class="text-gray-300 leading-relaxed mb-4">
                                Using the provided test graph data, the implementation produced:
                            </p>
                            <div class="bg-gradient-to-r from-pink-500/10 to-rose-500/10 border border-pink-500/20 rounded-xl p-6">
                                <div class="space-y-3">
                                    <div>
                                        <span class="text-pink-400 font-semibold">Optimal Path:</span>
                                        <span class="text-gray-300 ml-2 font-mono">{17, 23, 33, 41, 53, 56, 57, 60, 67, 70, 73, 76, 85, 89, 99}</span>
                                    </div>
                                    <div>
                                        <span class="text-pink-400 font-semibold">Minimum Cost:</span>
                                        <span class="text-gray-300 ml-2 font-mono">194.22</span>
                                    </div>
                                </div>
                            </div>
                            <p class="text-gray-300 leading-relaxed mt-4">
                                This confirms the algorithm correctly computes both the optimal policy (via <em>J</em>) and the associated optimal route (via greedy recovery using <em>J</em>).
                            </p>
                        </div>

                        <!-- Why This Project Matters -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Why This Project Matters</h2>
                            <p class="text-gray-300 leading-relaxed mb-6">
                                This project demonstrates the ability to:
                            </p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-pink-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Translate algorithmic theory into working code</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-pink-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Implement dynamic programming and iterative optimization methods</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-pink-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Handle real input parsing and edge cases (missing connections, indexing, Infinity handling)</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-pink-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Build an end-to-end solution that outputs interpretable results</span>
                                </div>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <h3 class="text-lg font-semibold text-pink-400 mb-3">Real-World Applications</h3>
                                <div class="flex flex-wrap gap-2">
                                    <span class="px-3 py-1 bg-zinc-700/50 rounded-full text-xs text-gray-300">Routing problems (transport, logistics)</span>
                                    <span class="px-3 py-1 bg-zinc-700/50 rounded-full text-xs text-gray-300">Network optimization</span>
                                    <span class="px-3 py-1 bg-zinc-700/50 rounded-full text-xs text-gray-300">Planning and decision-making under costs</span>
                                </div>
                            </div>
                        </div>

                        <!-- Tools & Skills -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Tools & Skills</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h3 class="text-lg font-semibold text-pink-400 mb-3">Tools</h3>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Mathematica</span>
                                    </div>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-pink-400 mb-3">Skills</h3>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Dynamic Programming</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Bellman Iteration</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Graph Optimization</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Shortest Path</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Data Parsing</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Algorithmic Implementation</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Code Structure -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Code Structure (Modules)</h2>
                            <div class="space-y-4">
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-pink-400 mb-2">dataToMatrix[filePath]</h3>
                                    <p class="text-gray-300 text-sm">Import graph & build distance matrix <em>Q</em></p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-pink-400 mb-2">bellmanIteration[Q, Jn]</h3>
                                    <p class="text-gray-300 text-sm">Compute Bellman update <em>J<sub>n+1</sub></em></p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-pink-400 mb-2">findCostToGo[Q, maxIter, tol]</h3>
                                    <p class="text-gray-300 text-sm">Iterate until convergence to final <em>J</em></p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-pink-400 mb-2">findPathAndTotalCost[Q, J, startNode]</h3>
                                    <p class="text-gray-300 text-sm">Recover optimal path + total cost</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Growth Model Project Page -->
        <div id="page-growth-model-project" class="page-content">
            <div class="pt-28 md:pt-32 pb-12 md:pb-20 px-4 md:px-6">
                <div class="max-w-6xl mx-auto">
                    <div class="mb-12">
                        <div class="mb-6">
                            <button onclick="showPage('projects')" class="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                                </svg>
                                <span class="font-medium">Back to Projects</span>
                            </button>
                        </div>
                        <div class="flex flex-col md:flex-row items-start justify-between gap-4 mb-6">
                            <div class="flex-1 min-w-0">
                                <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-2 md:mb-4">Solving a Growth Model Using Shooting and Genetic Algorithms</h1>
                                <p class="text-gray-400 text-base md:text-lg">A comparison of classical optimization methods versus evolutionary algorithms in solving dynamic economic models</p>
                            </div>
                            <div class="flex-shrink-0 w-full md:w-auto">
                                <a href="/EC3307Algorithms.nb" download class="px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                    </svg>
                                    Download Notebook
                                </a>
                            </div>
                        </div>
                        
                        <!-- Overview -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Overview</h2>
                            <p class="text-gray-300 text-lg leading-relaxed mb-4">
                                This project solves a deterministic neoclassical growth model using two fundamentally different numerical approaches: a shooting algorithm and a genetic algorithm. The objective is to compute the transition path of capital from an initial condition to its steady state and to compare the convergence, stability, and behavior of classical optimization methods versus evolutionary algorithms.
                            </p>
                            <p class="text-gray-300 leading-relaxed">
                                The project combines economic theory, numerical optimization, and computational experimentation, highlighting the trade-offs between structure-exploiting and search-based solution methods.
                            </p>
                        </div>

                        <!-- Model Framework -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Model Framework</h2>
                            <p class="text-gray-300 leading-relaxed mb-6">
                                The underlying model is a standard infinite-horizon growth model with capital accumulation and Cobb–Douglas production. A representative household maximizes discounted utility subject to a budget constraint, while firms maximize profits in competitive markets.
                            </p>
                            <div class="space-y-4 mb-6">
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-emerald-400 mb-3">Production Function</h3>
                                    <p class="text-gray-300 font-mono text-sm mb-2">
                                        <em>Y<sub>t</sub></em> = <em>K<sub>t</sub><sup>α</sup></em>(<em>AL<sub>t</sub></em>)<sup>1-α</sup>
                                    </p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h3 class="text-lg font-semibold text-emerald-400 mb-3">Capital Evolution</h3>
                                    <p class="text-gray-300 font-mono text-sm mb-2">
                                        <em>K<sub>t+1</sub></em> = (1 - δ)<em>K<sub>t</sub></em> + <em>I<sub>t</sub></em>
                                    </p>
                                </div>
                            </div>
                            <h3 class="text-xl font-bold mb-4 text-emerald-400">Key Parameters</h3>
                            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Capital Share (α)</div>
                                    <div class="text-gray-300">0.33</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Discount Factor (β)</div>
                                    <div class="text-gray-300">0.98</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Depreciation (δ)</div>
                                    <div class="text-gray-300">0.1</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Technology (A)</div>
                                    <div class="text-gray-300">1</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Initial Capital (K₀)</div>
                                    <div class="text-gray-300">0.1</div>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-4">
                                    <div class="text-emerald-400 font-bold mb-1">Time Horizon (T)</div>
                                    <div class="text-gray-300">70</div>
                                </div>
                            </div>
                        </div>

                        <!-- Analytical Foundations -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Analytical Foundations</h2>
                            <p class="text-gray-300 leading-relaxed mb-4">
                                Before implementing numerical solutions, the project:
                            </p>
                            <div class="space-y-3">
                                <div class="flex gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <p class="text-gray-300">Fully defines the competitive equilibrium</p>
                                </div>
                                <div class="flex gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <p class="text-gray-300">Derives the first-order conditions for households and firms</p>
                                </div>
                                <div class="flex gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <p class="text-gray-300">Obtains the Euler equation governing optimal consumption and capital accumulation</p>
                                </div>
                                <div class="flex gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <p class="text-gray-300">Solves analytically for the steady-state capital stock <em>K*</em></p>
                                </div>
                            </div>
                            <p class="text-gray-300 leading-relaxed mt-4">
                                This analytical groundwork ensures that numerical solutions can be evaluated against correct theoretical benchmarks.
                            </p>
                        </div>

                        <!-- Shooting Algorithm -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Shooting Algorithm</h2>
                            <div class="mb-6">
                                <h3 class="text-xl font-bold mb-4 text-emerald-400">Methodology</h3>
                                <p class="text-gray-300 leading-relaxed mb-4">
                                    The shooting algorithm solves the model by exploiting the Euler equation directly. Starting from an initial guess for the capital path, the algorithm iterates forward and adjusts guesses until the terminal condition—convergence to the steady state—is satisfied.
                                </p>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <h4 class="text-sm font-semibold text-emerald-400 mb-3">Implementation Details:</h4>
                                    <ul class="text-sm text-gray-300 space-y-2">
                                        <li>• Solving a system of nonlinear equations using FindRoot</li>
                                        <li>• Iterating capital forward over 70 periods</li>
                                        <li>• Ensuring convergence to the analytically derived steady state</li>
                                    </ul>
                                </div>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold mb-4 text-emerald-400">Results</h3>
                                <p class="text-gray-300 leading-relaxed">
                                    The shooting algorithm produces a smooth and monotonic transition path for capital. Capital converges steadily toward the steady-state level, closely matching theoretical predictions. This method serves as a benchmark solution due to its precision and stability.
                                </p>
                            </div>
                        </div>

                        <!-- Genetic Algorithm -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Genetic Algorithm</h2>
                            <div class="mb-6">
                                <h3 class="text-xl font-bold mb-4 text-emerald-400">Motivation</h3>
                                <p class="text-gray-300 leading-relaxed">
                                    To explore a model-agnostic alternative, the same growth model is solved using a genetic algorithm. Unlike the shooting method, the genetic algorithm does not directly impose the Euler equation. Instead, it searches over possible savings paths and evaluates them based on lifetime utility.
                                </p>
                            </div>
                            <div class="mb-6">
                                <h3 class="text-xl font-bold mb-4 text-emerald-400">Fitness Function</h3>
                                <p class="text-gray-300 leading-relaxed mb-4">
                                    A custom fitness function is defined to:
                                </p>
                                <ul class="list-disc list-inside space-y-2 text-gray-300 ml-4">
                                    <li>Simulate capital, output, consumption, and investment paths</li>
                                    <li>Compute discounted lifetime utility</li>
                                    <li>Penalize paths that fail to converge to the steady state after <em>T</em> periods</li>
                                </ul>
                                <p class="text-gray-300 leading-relaxed mt-4">
                                    This ensures that only economically meaningful solutions achieve high fitness scores.
                                </p>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold mb-4 text-emerald-400">Genetic Algorithm Structure</h3>
                                <p class="text-gray-300 leading-relaxed mb-4">
                                    The implementation includes all core evolutionary components:
                                </p>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Selection</div>
                                        <div class="text-gray-300 text-sm">Retains the top 50% of solutions by fitness</div>
                                    </div>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Parent Selection</div>
                                        <div class="text-gray-300 text-sm">Probabilistic selection weighted by fitness</div>
                                    </div>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Crossover</div>
                                        <div class="text-gray-300 text-sm">Binary encoding with random crossover points</div>
                                    </div>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Mutation</div>
                                        <div class="text-gray-300 text-sm">Bit-flipping with a 2.5% mutation rate</div>
                                    </div>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Population Size</div>
                                        <div class="text-gray-300 text-sm">80</div>
                                    </div>
                                    <div class="bg-zinc-800/30 rounded-xl p-4">
                                        <div class="text-emerald-400 font-bold mb-2">Generations</div>
                                        <div class="text-gray-300 text-sm">1000+</div>
                                    </div>
                                </div>
                                <p class="text-gray-300 leading-relaxed mt-4">
                                    The algorithm tracks both mean fitness and maximum fitness across generations, allowing analysis of convergence behavior.
                                </p>
                            </div>
                        </div>

                        <!-- Results and Comparison -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Results and Comparison</h2>
                            <div class="space-y-6">
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-emerald-400">Capital Stock Dynamics</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        The shooting algorithm generates a smooth and stable capital path that converges monotonically to the steady state. In contrast, the genetic algorithm produces a much noisier capital trajectory. While capital fluctuates significantly due to stochastic mutation and crossover, it still converges toward a level close to the steady state.
                                    </p>
                                    <p class="text-gray-300 leading-relaxed">
                                        These fluctuations reflect the exploratory nature of genetic algorithms, which trade precision for flexibility and global search capability.
                                    </p>
                                </div>
                                <div>
                                    <h3 class="text-xl font-bold mb-4 text-emerald-400">Savings Rate Behavior</h3>
                                    <p class="text-gray-300 leading-relaxed mb-4">
                                        The difference between the two methods is even more pronounced when examining savings rates.
                                    </p>
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div class="bg-zinc-800/30 rounded-xl p-5">
                                            <h4 class="text-lg font-semibold text-emerald-400 mb-2">Shooting Algorithm</h4>
                                            <p class="text-gray-300 text-sm">Produces a smooth, declining savings rate consistent with optimal intertemporal behavior</p>
                                        </div>
                                        <div class="bg-zinc-800/30 rounded-xl p-5">
                                            <h4 class="text-lg font-semibold text-emerald-400 mb-2">Genetic Algorithm</h4>
                                            <p class="text-gray-300 text-sm">Produces a highly volatile savings rate, though its average level aligns broadly with the shooting solution</p>
                                        </div>
                                    </div>
                                    <p class="text-gray-300 leading-relaxed mt-4">
                                        This highlights a key trade-off: genetic algorithms can approximate optimal policies without explicit analytical conditions, but at the cost of short-run stability.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Key Takeaways -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Key Takeaways</h2>
                            <div class="space-y-4">
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <p class="text-gray-300">The shooting algorithm is highly efficient and precise when analytical structure is available.</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <p class="text-gray-300">The genetic algorithm provides a flexible, model-agnostic optimization framework.</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <p class="text-gray-300">Despite its stochastic nature, the genetic algorithm converges toward economically meaningful solutions.</p>
                                </div>
                                <div class="bg-zinc-800/30 rounded-xl p-5">
                                    <p class="text-gray-300">Increasing population size, running more generations, or reducing mutation rates would likely improve stability and convergence.</p>
                                </div>
                            </div>
                        </div>

                        <!-- Why This Project Matters -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Why This Project Matters</h2>
                            <p class="text-gray-300 leading-relaxed mb-6">
                                This project demonstrates the ability to:
                            </p>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Translate economic theory into computational solutions</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Implement and compare fundamentally different optimization techniques</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Design fitness functions and convergence criteria</span>
                                </div>
                                <div class="flex items-start gap-3">
                                    <svg class="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span class="text-gray-300">Interpret numerical results through an economic lens</span>
                                </div>
                            </div>
                            <p class="text-gray-300 leading-relaxed mt-6">
                                The comparison highlights the strengths and limitations of both classical numerical methods and evolutionary algorithms in dynamic optimization problems.
                            </p>
                        </div>

                        <!-- Tools & Skills -->
                        <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                            <h2 class="text-2xl sm:text-3xl font-bold mb-6">Tools & Skills</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <h3 class="text-lg font-semibold text-emerald-400 mb-3">Tools</h3>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Mathematica</span>
                                    </div>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-emerald-400 mb-3">Skills</h3>
                                    <div class="flex flex-wrap gap-2">
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Shooting Algorithm</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Genetic Algorithm</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Economic Modeling</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Numerical Optimization</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Dynamic Programming</span>
                                        <span class="px-3 py-1 bg-zinc-800/50 rounded-full text-sm text-gray-300">Computational Economics</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        let currentPage = 'home';
        let activeSection = 'about';
        
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1044',message:'Script initialization',data:{currentPage:currentPage,activeSection:activeSection,documentReady:document.readyState},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
        // #endregion
        
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            
            if (sidebar.classList.contains('sidebar-closed')) {
                sidebar.classList.remove('sidebar-closed');
                sidebar.classList.add('sidebar-open');
                overlay.classList.remove('hidden');
            } else {
                sidebar.classList.add('sidebar-closed');
                sidebar.classList.remove('sidebar-open');
                overlay.classList.add('hidden');
            }
        }
        
        function showPage(page) {
            // #region agent log
            fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1062',message:'showPage called',data:{page:page,previousPage:currentPage},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
            // #endregion
            
            currentPage = page;
            
            // Hide all pages
            document.querySelectorAll('.page-content').forEach(p => {
                p.classList.remove('active');
            });
            
            // Show selected page (handle special cases)
            if (page === 'academic-work') {
                // Don't show academic-work page directly, it's handled by showAcademicWork
                return;
            } else {
            document.getElementById('page-' + page).classList.add('active');
            }
            
            // Update menu items
            document.querySelectorAll('.menu-item').forEach(item => {
                const itemPage = item.getAttribute('data-page');
                if (itemPage === page) {
                    item.classList.add('active');
                    item.classList.remove('text-gray-400');
                } else {
                    item.classList.remove('active');
                    item.classList.add('text-gray-400');
                }
            });
            
            // Show/hide home nav and back button
            const homeNav = document.getElementById('home-nav');
            const backBtn = document.getElementById('back-home-btn');
            
            // #region agent log
            fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1085',message:'Before button visibility logic',data:{page:page,homeNavFound:!!homeNav,backBtnFound:!!backBtn,backBtnClasses:backBtn?Array.from(backBtn.classList).join(' '):'null'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
            // #endregion
            
            if (page === 'home') {
                homeNav.classList.remove('hidden');
                homeNav.classList.add('md:flex');
                backBtn.classList.add('hidden');
                backBtn.classList.remove('md:flex');
                
                // #region agent log
                fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1091',message:'After hiding back button (home page)',data:{backBtnClasses:backBtn?Array.from(backBtn.classList).join(' '):'null'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
                // #endregion
            } else {
                homeNav.classList.add('hidden');
                homeNav.classList.remove('md:flex');
                backBtn.classList.remove('hidden');
                backBtn.classList.add('md:flex');
                
                // #region agent log
                fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1097',message:'After showing back button (non-home page)',data:{backBtnClasses:backBtn?Array.from(backBtn.classList).join(' '):'null'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
                // #endregion
            }
            
            // Load academic works list when showing academic-works page
            if (page === 'academic-works') {
                loadAcademicWorksList();
            }
            
            // Close sidebar
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            sidebar.classList.add('sidebar-closed');
            sidebar.classList.remove('sidebar-open');
            overlay.classList.add('hidden');
            
            // Scroll to top
            window.scrollTo(0, 0);
        }
        
        // Academic Works Data Structure
        const academicWorks = [
            {
                id: 'labour-economics-returns',
                title: 'Regional differences in returns to higher education within the United Kingdom',
                subtitle: 'An empirical analysis of educational returns across UK regions',
                category: 'Research Paper',
                year: '2024',
                tags: ['Labour Economics', 'Education', 'Regional Analysis', 'Econometrics'],
                description: 'This study examines regional differences in the returns to higher education within the United Kingdom using data from the 2011 Quarterly Labour Force Survey (QLFS). The analysis employs Ordinary Least Squares (OLS) and Instrumental Variables (IV) regression to estimate the economic returns to schooling while addressing potential biases such as endogeneity and omitted variables.',
                pdfPath: '/EC4411-Labour-Economics-Project-Final.pdf',
                content: `
                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Abstract</h2>
                        <p class="text-gray-300 text-lg leading-relaxed mb-4">
                            This study examines regional differences in the returns to higher education within the United Kingdom using data from the 2011 Quarterly Labour Force Survey (QLFS). The analysis employs Ordinary Least Squares (OLS) and Instrumental Variables (IV) regression to estimate the economic returns to schooling while addressing potential biases such as endogeneity and omitted variables. Key findings highlight substantial variation in returns across regions, with evidence suggesting that OLS underestimates the true effect of education on wages. These results contribute to understanding geographic disparities in educational outcomes, providing insights for policymakers focused on regional economic inequality and education policy.
                        </p>
                        <div class="mt-4 text-sm text-gray-400">
                            <p><strong>Date:</strong> 12 December 2024</p>
                            <p><strong>Course:</strong> EC4411 - Labour Economics</p>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Research Question</h2>
                        <p class="text-gray-300 text-lg leading-relaxed mb-4">
                            Do returns to higher education differ significantly between London and other regions in the UK?
                        </p>
                        <p class="text-gray-300 leading-relaxed">
                            The hypothesis underpinning this research is that the returns to secondary and higher education are higher in London due to its concentration of high-skilled industries, professional job opportunities, and higher living costs, which may inflate wages.
                        </p>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Methodology</h2>
                        <div class="space-y-4">
                            <div>
                                <h3 class="text-xl font-bold mb-3 text-violet-400">Data Source</h3>
                                <p class="text-gray-300">2011 Quarterly Labour Force Survey (QLFS)</p>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold mb-3 text-violet-400">Estimation Methods</h3>
                                <ul class="list-disc list-inside text-gray-300 space-y-2">
                                    <li>Mincer earnings equation with OLS regression</li>
                                    <li>Instrumental Variables (IV) approach using mother's occupation (ses_rank) as an instrument</li>
                                    <li>Regional interaction terms to capture London-specific effects</li>
                                </ul>
                            </div>
                            <div>
                                <h3 class="text-xl font-bold mb-3 text-violet-400">Key Variables</h3>
                                <p class="text-gray-300">Years of schooling, educational attainment milestones (secondary and higher education), work experience, gender, and regional indicators</p>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Key Findings</h2>
                        <div class="space-y-4">
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-lg font-semibold text-violet-400 mb-2">OLS Results</h3>
                                <p class="text-gray-300">4.1% return for each additional year of schooling. Premiums for secondary and higher education are notably higher in London compared to other regions.</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-lg font-semibold text-violet-400 mb-2">Regional Disparities</h3>
                                <p class="text-gray-300">Significant regional disparities in returns to education, with London demonstrating higher returns to educational qualifications due to its concentration of high-skilled industries and professional job opportunities.</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-lg font-semibold text-violet-400 mb-2">IV Analysis Limitations</h3>
                                <p class="text-gray-300">The instrumental variable approach yielded imprecise estimates due to weak instrument problem (F-statistic of 2.43), highlighting the challenges of identifying robust causal effects in this context.</p>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Policy Implications</h2>
                        <p class="text-gray-300 leading-relaxed mb-4">
                            The findings suggest that investments in secondary and higher education remain critical for enhancing individual productivity and earnings potential. Policymakers should prioritize regional economic development initiatives that create high-skilled employment opportunities beyond London, thereby narrowing the gap in returns to education between regions.
                        </p>
                        <p class="text-gray-300 leading-relaxed">
                            In London, policies to address the high cost of living—such as affordable housing initiatives or transportation subsidies—could enhance the net benefits of higher education.
                        </p>
                    </div>
                `
            },
            {
                id: 'referee-report',
                title: 'Referee Report: Digital Addiction',
                subtitle: 'Critical analysis of Allcott, Gentzkow & Song (2022)',
                category: 'Referee Report',
                year: '2024',
                tags: ['Academic Review', 'Behavioral Economics', 'Causal Inference', 'RCT Analysis'],
                description: 'A comprehensive referee report on "Digital Addiction" (AER, 2022), critically evaluating a large-scale randomized controlled trial that examines habit formation and self-control mechanisms in smartphone and social media use, with a focus on causal identification and behavioral responses.',
                pdfPath: '/EC4425-RefereeReportFinal-copy.pdf',
                content: `
                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Overview</h2>
                        <p class="text-gray-300 text-lg leading-relaxed mb-4">
                            This project involved writing a full referee report on <strong class="text-violet-400">"Digital Addiction"</strong> (American Economic Review, 2022) by Allcott, Gentzkow & Song, a leading empirical paper studying habit formation and self-control in smartphone and social media use. The paper combines a large-scale randomized controlled trial with behavioral economic theory to quantify the mechanisms driving digital addiction.
                        </p>
                        <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <div class="text-violet-400 font-bold mb-1">Course</div>
                                <div class="text-gray-300">EC4425</div>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <div class="text-violet-400 font-bold mb-1">Paper</div>
                                <div class="text-gray-300">AER 2022</div>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <div class="text-violet-400 font-bold mb-1">Sample Size</div>
                                <div class="text-gray-300">~2,000 Android users</div>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">What the Paper Studies</h2>
                        <p class="text-gray-300 leading-relaxed mb-6">
                            The authors investigate whether excessive smartphone use is driven by:
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Habit Formation</h3>
                                </div>
                                <p class="text-gray-300 text-sm">Persistent behavioral change resulting from repeated smartphone use</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Self-Control Problems</h3>
                                </div>
                                <p class="text-gray-300 text-sm">Difficulty aligning actual and ideal usage patterns</p>
                            </div>
                        </div>
                        <p class="text-gray-300 leading-relaxed">
                            Using a randomized experiment with nearly 2,000 Android users, the study evaluates the effects of <strong class="text-violet-400">financial incentives</strong> and <strong class="text-violet-400">app-based usage limits</strong> on screen time, subjective well-being, and self-reported addiction.
                        </p>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">My Contribution</h2>
                        <p class="text-gray-300 leading-relaxed mb-6">
                            In my referee report, I critically evaluated:
                        </p>
                        <div class="space-y-4">
                            <div class="flex gap-4">
                                <div class="w-8 h-8 bg-violet-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-gray-200 mb-2">Experimental Design & Identification</h3>
                                    <p class="text-gray-400">Critical assessment of the RCT design and identification strategy</p>
                                </div>
                            </div>
                            <div class="flex gap-4">
                                <div class="w-8 h-8 bg-violet-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-gray-200 mb-2">Causal Claims & Balance Assumptions</h3>
                                    <p class="text-gray-400">Evaluation of the validity of causal claims and balance assumptions</p>
                                </div>
                            </div>
                            <div class="flex gap-4">
                                <div class="w-8 h-8 bg-violet-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-gray-200 mb-2">Treatment Effects Analysis</h3>
                                    <p class="text-gray-400">Examination of effects on screen time, well-being, and addiction measures</p>
                                </div>
                            </div>
                            <div class="flex gap-4">
                                <div class="w-8 h-8 bg-violet-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <h3 class="text-lg font-semibold text-gray-200 mb-2">Transparency & Robustness</h3>
                                    <p class="text-gray-400">Assessment of transparency, robustness checks, and deviations from pre-analysis plan</p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-6 bg-zinc-800/30 rounded-xl p-5">
                            <h3 class="text-lg font-semibold text-violet-400 mb-3">Validity Assessment</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <h4 class="text-sm font-semibold text-gray-300 mb-2">Internal Validity</h4>
                                    <ul class="text-sm text-gray-400 space-y-1">
                                        <li>• Randomization checks</li>
                                        <li>• Attrition analysis</li>
                                        <li>• Compliance assessment</li>
                                        <li>• Spillover effects</li>
                                    </ul>
                                </div>
                                <div>
                                    <h4 class="text-sm font-semibold text-gray-300 mb-2">External Validity</h4>
                                    <ul class="text-sm text-gray-400 space-y-1">
                                        <li>• Sample representativeness</li>
                                        <li>• Pandemic context considerations</li>
                                        <li>• Generalizability concerns</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Key Findings Discussed</h2>
                        <div class="space-y-4">
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Habit Formation Evidence</h3>
                                </div>
                                <p class="text-gray-300">Temporary financial incentives produced persistent reductions in screen time, supporting the habit formation mechanism</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Self-Control Problems</h3>
                                </div>
                                <p class="text-gray-300">App-based limits consistently reduced usage, highlighting ongoing self-control problems among users</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Well-Being & Addiction</h3>
                                </div>
                                <p class="text-gray-300">Both interventions reduced self-reported addiction, with modest improvements in subjective well-being</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-5">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center">
                                        <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                                        </svg>
                                    </div>
                                    <h3 class="text-lg font-semibold text-gray-200">Substitution Patterns</h3>
                                </div>
                                <p class="text-gray-300">Different treatments induced distinct substitution patterns across apps and devices</p>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Critical Evaluation & Extensions</h2>
                        <p class="text-gray-300 leading-relaxed mb-6">
                            The report highlights strengths in transparency and methodological rigor, while also proposing extensions such as:
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-sm font-semibold text-violet-400 mb-2">Baseline Data</h3>
                                <p class="text-gray-300 text-sm">Using pre-installation smartphone usage data to strengthen baseline comparisons</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-sm font-semibold text-violet-400 mb-2">Temporal Validity</h3>
                                <p class="text-gray-300 text-sm">Replicating the experiment outside the COVID-19 period to test temporal generalizability</p>
                            </div>
                            <div class="bg-zinc-800/30 rounded-xl p-4">
                                <h3 class="text-sm font-semibold text-violet-400 mb-2">Platform Extension</h3>
                                <p class="text-gray-300 text-sm">Expanding analysis to iOS users to test external validity across platforms</p>
                            </div>
                        </div>
                    </div>

                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50 mb-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-6">Skills Demonstrated</h2>
                        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Causal Inference</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">RCT Analysis</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Critical Evaluation</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Behavioral Economics</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Digital Welfare</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Data Interpretation</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Robustness Analysis</span>
                            <span class="px-4 py-2 bg-violet-500/10 text-violet-400 rounded-full text-sm font-medium text-center">Analytical Writing</span>
                        </div>
                    </div>

                    <div class="bg-gradient-to-r from-violet-500/10 to-purple-500/10 border border-violet-500/20 rounded-3xl p-8">
                        <h2 class="text-2xl sm:text-3xl font-bold mb-4">Full Report Available</h2>
                        <p class="text-gray-300 leading-relaxed mb-6">
                            For a comprehensive analysis including detailed methodological critique, specific findings evaluation, and detailed recommendations, please download the full referee report PDF below. The complete document provides in-depth examination of all aspects of the research under review.
                        </p>
                        <div class="flex items-center gap-2 text-violet-400">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span class="text-sm font-medium">Download the PDF to access the complete detailed analysis</span>
                        </div>
                    </div>
                `
            }
        ];
        
        function loadAcademicWorksList() {
            const listContainer = document.getElementById('academic-works-list');
            if (!listContainer) return;
            
            // Clear placeholder
            listContainer.innerHTML = '';
            
            if (academicWorks.length === 0) {
                listContainer.innerHTML = `
                    <div class="col-span-full text-center py-12">
                        <p class="text-gray-400">No academic works available yet.</p>
                    </div>
                `;
                return;
            }
            
            academicWorks.forEach(work => {
                const workCard = document.createElement('div');
                workCard.className = 'glass-card rounded-3xl overflow-hidden border border-zinc-800/50 card-hover flex flex-col h-full';
                workCard.innerHTML = `
                    <div class="p-4 md:p-6 flex flex-col h-full">
                        <div class="mb-3">
                            <div class="inline-block px-3 py-1 bg-blue-500/10 text-blue-400 rounded-full text-xs font-medium mb-3">
                                ${work.category || 'Academic Paper'}
                            </div>
                            <h3 class="text-xl md:text-2xl font-bold mb-2 leading-tight">${work.title}</h3>
                        </div>
                        <p class="text-gray-400 mb-4 text-sm md:text-base leading-relaxed flex-grow">${work.description || work.subtitle || ''}</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            ${work.tags ? work.tags.map(tag => `<span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">${tag}</span>`).join('') : ''}
                            ${work.year ? `<span class="px-3 py-1 bg-zinc-800/50 rounded-full text-xs text-gray-300">${work.year}</span>` : ''}
                        </div>
                        <button onclick="showAcademicWork('${work.id}')" class="w-full px-4 py-2 bg-zinc-800/50 hover:bg-zinc-700/50 rounded-xl transition-colors font-medium mt-auto">View Work</button>
                    </div>
                `;
                listContainer.appendChild(workCard);
            });
        }
        
        function showAcademicWork(workId) {
            const work = academicWorks.find(w => w.id === workId);
            if (!work) {
                console.error('Academic work not found:', workId);
                return;
            }
            
            currentPage = 'academic-work';
            
            // Hide all pages
            document.querySelectorAll('.page-content').forEach(p => {
                p.classList.remove('active');
            });
            
            // Show academic work page
            document.getElementById('page-academic-work').classList.add('active');
            
            // Update title and subtitle
            document.getElementById('academic-work-title').textContent = work.title;
            document.getElementById('academic-work-subtitle').textContent = work.subtitle || work.description || '';
            
            // Update download buttons
            const downloadContainer = document.getElementById('academic-work-download');
            downloadContainer.innerHTML = '';
            if (work.pdfPath) {
                const downloadBtn = document.createElement('a');
                downloadBtn.href = work.pdfPath;
                downloadBtn.download = true;
                downloadBtn.className = 'px-6 py-3 bg-violet-500 hover:bg-violet-600 rounded-xl font-medium transition-colors flex items-center gap-2';
                downloadBtn.innerHTML = `
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    Download PDF
                `;
                downloadContainer.appendChild(downloadBtn);
            }
            
            // Update content
            const contentContainer = document.getElementById('academic-work-content');
            if (work.content) {
                contentContainer.innerHTML = work.content;
            } else {
                contentContainer.innerHTML = `
                    <div class="glass-card rounded-3xl p-8 border border-zinc-800/50">
                        <p class="text-gray-400">Content for this academic work will be displayed here.</p>
                    </div>
                `;
            }
            
            // Update menu items (keep academic-works active)
            document.querySelectorAll('.menu-item').forEach(item => {
                const itemPage = item.getAttribute('data-page');
                if (itemPage === 'academic-works') {
                    item.classList.add('active');
                    item.classList.remove('text-gray-400');
                } else {
                    item.classList.remove('active');
                    item.classList.add('text-gray-400');
                }
            });
            
            // Show back button, hide home nav
            const homeNav = document.getElementById('home-nav');
            const backBtn = document.getElementById('back-home-btn');
            homeNav.classList.add('hidden');
            homeNav.classList.remove('md:flex');
            backBtn.classList.remove('hidden');
            backBtn.classList.add('md:flex');
            
            // Close sidebar
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            sidebar.classList.add('sidebar-closed');
            sidebar.classList.remove('sidebar-open');
            overlay.classList.add('hidden');
            
            // Scroll to top
            window.scrollTo(0, 0);
        }
        
        function scrollToSection(section) {
            activeSection = section;
            document.getElementById(section)?.scrollIntoView({ behavior: 'smooth' });
            updateNavButtons();
        }
        
        function updateNavButtons() {
            const buttons = document.querySelectorAll('.nav-pill');
            buttons.forEach(btn => {
                const onclickStr = btn.getAttribute('onclick');
                const section = onclickStr.match(/'([^']+)'/)[1];
                if (section === activeSection) {
                    btn.className = 'nav-pill active px-5 py-2 rounded-full text-sm font-medium';
                } else {
                    btn.className = 'nav-pill px-5 py-2 rounded-full text-sm font-medium text-gray-400';
                }
            });
        }
        
        function toggleAboutMe() {
            const preview = document.getElementById('about-preview');
            const full = document.getElementById('about-full');
            const button = document.getElementById('about-read-more-btn');
            
            if (preview && full && button) {
                if (full.classList.contains('hidden')) {
                    // Show full text
                    preview.classList.add('hidden');
                    full.classList.remove('hidden');
                    button.innerHTML = `
                        <span>Read less</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                        </svg>
                    `;
                } else {
                    // Show preview
                    preview.classList.remove('hidden');
                    full.classList.add('hidden');
                    button.innerHTML = `
                        <span>Read more</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                    `;
                }
            }
        }
        
        // Update active section based on scroll position
        const observerOptions = {
            root: null,
            rootMargin: '-50% 0px -50% 0px',
            threshold: 0
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && currentPage === 'home') {
                    activeSection = entry.target.id;
                    updateNavButtons();
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('section').forEach(section => {
            observer.observe(section);
        });
        
        // Initialize button state on page load (ensure back button is hidden on home page)
        function initializeButtonState() {
            const backBtn = document.getElementById('back-home-btn');
            const homeNav = document.getElementById('home-nav');
            if (currentPage === 'home') {
                if (backBtn) {
                    backBtn.classList.add('hidden');
                    backBtn.classList.remove('md:flex');
                }
                if (homeNav) {
                    homeNav.classList.remove('hidden');
                    homeNav.classList.add('md:flex');
                }
            }
        }
        
        // Initialize on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeButtonState);
        } else {
            initializeButtonState();
        }
        
        // #region agent log
        // Check initial state on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                const backBtn = document.getElementById('back-home-btn');
                const homeNav = document.getElementById('home-nav');
                fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1150',message:'DOMContentLoaded - initial state check',data:{currentPage:currentPage,backBtnFound:!!backBtn,backBtnClasses:backBtn?Array.from(backBtn.classList).join(' '):'null',homeNavFound:!!homeNav,homeNavClasses:homeNav?Array.from(homeNav.classList).join(' '):'null',showPageCalled:typeof showPage==='function'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
            });
        } else {
            const backBtn = document.getElementById('back-home-btn');
            const homeNav = document.getElementById('home-nav');
            fetch('http://127.0.0.1:7242/ingest/5b00a031-865a-4a49-ab64-e64bef3ea0c5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'app.py:1158',message:'DOM already ready - initial state check',data:{currentPage:currentPage,backBtnFound:!!backBtn,backBtnClasses:backBtn?Array.from(backBtn.classList).join(' '):'null',homeNavFound:!!homeNav,homeNavClasses:homeNav?Array.from(homeNav.classList).join(' '):'null'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
        }
        // #endregion
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/The-Comeback-King-F1s-Greatest-Position-Gainer.pdf')
def download_pdf():
    return send_from_directory('static', 'The-Comeback-King-F1s-Greatest-Position-Gainer.pdf', as_attachment=True)

@app.route('/IE_CV.pdf')
def download_cv():
    return send_from_directory('static', 'IE_CV.pdf', as_attachment=True)

@app.route('/EC4411-Labour-Economics-Project-Final.pdf')
def download_labour_economics():
    return send_from_directory('static', 'EC4411 Labour Economics Project Final.pdf', as_attachment=True)

@app.route('/EC4425-RefereeReportFinal-copy.pdf')
def download_referee_report():
    return send_from_directory('static', 'EC4425-RefereeReportFinal copy.pdf', as_attachment=True)

@app.route('/Project1_Final.ipynb')
def download_timeseries_notebook():
    return send_from_directory('static', 'Project1_Final.ipynb', as_attachment=True)

@app.route('/co2.json')
def download_co2_data():
    return send_from_directory('static', 'co2.json', as_attachment=True)

@app.route('/EC3307Algorithms.nb')
def download_algorithms_notebook():
    return send_from_directory('static', 'EC3307Algorithms.nb', as_attachment=True)

@app.route('/EC3307Graph.nb')
def download_graph_notebook():
    return send_from_directory('static', 'EC3307Graph.nb', as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
