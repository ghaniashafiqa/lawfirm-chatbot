<template>
  <div class="landing text-gray-800 font-sans scroll-smooth">

    <!-- Hero Section -->
    <section
      id="home"
      class="min-h-screen bg-gradient-to-br from-[#f9f6f4] to-white flex items-center px-6 py-20 relative overflow-hidden"
    >
      <div
        class="absolute inset-0 pointer-events-none opacity-5"
        style="background-image: url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22 fill=%22none%22 viewBox=%220 0 40 40%22><path stroke=%22%23d1d5db%22 stroke-width=%221%22 d=%22M0 0h40v40H0z%22/></svg>'); background-repeat: repeat;"
      ></div>

      <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center animate-fade-in">
        <!-- Text Content -->
        <div class="text-center md:text-left">
          <h1 class="text-5xl md:text-6xl font-serif font-bold text-neutral-900 leading-tight mb-6">
            Chatbot Hukum Pertanahan<br />
            <span class="text-primary">untuk Informasi & Bantuan</span>
          </h1>
          <p class="text-lg text-gray-700 mb-8 leading-relaxed">
            Dapatkan informasi hukum terpercaya seputar <strong>sengketa tanah</strong>, sertifikasi, dan pencegahan mafia tanah.
            Chatbot ini dikembangkan bersama <strong>SAP Lawfirm</strong> dan <strong>Gebukmantan.com</strong>.
          </p>
          <router-link to="/chat">
            <button class="inline-flex items-center gap-2 px-8 py-3 bg-primary text-white text-lg font-semibold rounded-md hover:bg-opacity-90 transition-all shadow-md">
              💬 Coba Hukum Cerdas
            </button>
          </router-link>
        </div>

        <!-- Hero Image -->
        <div class="relative hidden md:block">
          <img
            src="@/assets/lawyer-illustration.svg"
            alt="Ilustrasi Pengacara"
            class="w-full h-auto object-cover animate-fade-in-up"
          />
        </div>
      </div>
    </section>

    <!-- About Us Section -->
<section id="about" class="min-h-screen py-24 px-6 bg-white animate-fade-in">
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 items-center gap-12">
    <!-- Text Content -->
    <div>
      <h2 class="text-sm font-semibold text-red-700 uppercase tracking-wide mb-2">Tentang Proyek Ini</h2>
      <h3 class="text-4xl font-serif font-bold text-neutral-900 mb-6">
        Mewujudkan Akses Hukum yang Lebih Merata
      </h3>
      <p class="text-gray-700 leading-relaxed mb-4">
        Di tengah kompleksitas hukum pertanahan, banyak masyarakat kesulitan mendapatkan informasi yang akurat dan mudah dipahami. <strong>Hukum Cerdas</strong> hadir sebagai solusi digital yang menjembatani akses hukum dan literasi publik.
      </p>

      
    <div class="flex flex-wrap gap-2 my-6">
      <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">#Edukasi</span>
      <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">#Kolaborasi</span>
      <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">#AksesHukum</span>
      <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">#Inklusif</span>
      <span class="bg-primary text-white text-xs px-3 py-1 rounded-full">#Responsif</span>
    </div>

      <p class="text-gray-700 leading-relaxed">
        Proyek ini digagas bersama <strong>SAP Lawfirm</strong> dan <strong>Gebukmantan.com</strong>, menggabungkan keahlian hukum dengan pendekatan digital yang humanis dan edukatif.
      </p>
    </div>

    <!-- Images -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <img src="@/assets/office-1.jpg" class="rounded-xl shadow-md w-full h-64 object-cover" />
      <img src="@/assets/office-2.jpg" class="rounded-xl shadow-md w-full h-64 object-cover" />
    </div>
  </div>
</section>


    <!-- Divider -->
    <div class="h-12 bg-gradient-to-b from-white to-[#f9f6f4]"></div>

    <!-- Partner Websites -->
    <section id="partners" class="py-24 px-6 bg-[#f9f6f4] animate-fade-in-up">
      <div class="max-w-7xl mx-auto text-center mb-16">
        <h2 class="text-4xl font-bold font-serif text-neutral-900 mb-4">Mitra Kolaborasi</h2>
        <p class="text-lg text-gray-600">
          Hukum Cerdas didukung oleh mitra terpercaya yang berkontribusi dalam edukasi dan akses layanan hukum.
        </p>
      </div>

      <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
        <!-- SAP Lawfirm -->
        <div class="bg-white border border-neutral-200 rounded-2xl shadow-md hover:shadow-xl transition duration-300">
          <img src="@/assets/saplawfirm-preview.png" alt="SAP Lawfirm" class="w-full h-48 object-cover rounded-t-2xl" />
          <div class="p-6 text-left">
            <h3 class="text-xl font-semibold text-neutral-800 mb-2">SAP Lawfirm</h3>
            <p class="text-gray-600 text-sm mb-4">
              Kantor hukum profesional yang fokus pada isu pertanahan dan perlindungan hukum.
            </p>
            <a
              href="https://saplawfirm.com"
              target="_blank"
              class="inline-block px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-opacity-90 transition"
            >
              Kunjungi Situs
            </a>
          </div>
        </div>

        <!-- GebukMantan -->
        <div class="bg-white border border-neutral-200 rounded-2xl shadow-md hover:shadow-xl transition duration-300">
          <img src="@/assets/logo-lawfirm.png" alt="GebukMantan.com" class="w-full h-48 object-cover rounded-t-2xl" />
          <div class="p-6 text-left">
            <h3 class="text-xl font-semibold text-neutral-800 mb-2">GebukMantan.com</h3>
            <p class="text-gray-600 text-sm mb-4">
              Media digital dengan pendekatan kreatif untuk edukasi hukum pertanahan dan advokasi publik.
            </p>
            <a
              href="https://gebukmantan.com"
              target="_blank"
              class="inline-block px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-opacity-90 transition"
            >
              Kunjungi Situs
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="min-h-screen py-24 px-6 bg-white animate-fade-in">
      <div class="max-w-7xl mx-auto text-center mb-16">
        <h2 class="text-4xl font-serif font-bold text-neutral-900">Fitur Utama</h2>
        <p class="text-lg text-gray-600 mt-4">Didukung oleh SAP Lawfirm dan mitra terpercaya.</p>
      </div>

      <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
          <img src="@/assets/feature-docs.png" alt="Akses Dokumen" class="w-full h-64 object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
            <h3 class="text-white text-xl font-semibold mb-2">Akses Dokumen Hukum</h3>
            <p class="text-sm text-white/80">Informasi berdasarkan sumber hukum yang dapat dipercaya.</p>
          </div>
        </div>

        <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
          <img src="@/assets/feature-context.png" alt="Jawaban Kontekstual" class="w-full h-64 object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
            <h3 class="text-white text-xl font-semibold mb-2">Jawaban Sesuai Konteks</h3>
            <p class="text-sm text-white/80">Respons disesuaikan dengan pertanyaan dan kebutuhan pengguna.</p>
          </div>
        </div>

        <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
          <img src="@/assets/feature-247.png" alt="Tersedia 24/7" class="w-full h-64 object-cover" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
            <h3 class="text-white text-xl font-semibold mb-2">Layanan 24/7</h3>
            <p class="text-sm text-white/80">Bisa diakses kapan saja untuk informasi hukum umum.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-24 bg-primary text-white text-center px-6 relative overflow-hidden animate-fade-in-up">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl md:text-5xl font-serif font-bold mb-6 leading-snug">
          Dapatkan Informasi Hukum<br class="hidden md:block" /> dari Dokumen yang Terverifikasi
        </h2>
        <p class="text-lg text-white/90 mb-8">
          Gunakan Hukum Cerdas untuk memahami persoalan pertanahan, kebutuhan dokumen, dan langkah awal penyelesaian hukum Anda.
        </p>
        <router-link to="/chat">
          <button class="inline-flex items-center gap-2 px-8 py-3 bg-accent text-primary text-lg font-semibold rounded-md hover:bg-yellow-500 transition shadow-lg">
            💬 Chat Sekarang
          </button>
        </router-link>
      </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="py-24 px-6 bg-white animate-fade-in">
      <div class="max-w-5xl mx-auto text-center">
        <h2 class="text-4xl font-serif font-bold text-primary mb-12">Pertanyaan yang Sering Diajukan</h2>
        <FAQList />
      </div>
    </section>

    <!-- Contact Us -->
    <section id="contact" class="py-24 px-6 bg-neutralbg animate-fade-in-up">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl font-serif font-bold text-center text-primary mb-12">Hubungi Kami</h2>
        <form class="grid gap-4 md:grid-cols-2 bg-white p-10 rounded-xl shadow-xl">
          <input type="text" placeholder="Nama Anda" class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent" />
          <input type="email" placeholder="Email Anda" class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent" />
          <textarea rows="4" placeholder="Pesan atau masukan Anda" class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent"></textarea>
          <button type="submit" class="col-span-2 bg-primary text-white px-6 py-3 rounded-md hover:bg-opacity-90 transition shadow-md">
            Kirim Pesan
          </button>
        </form>
        <p class="text-center text-sm text-gray-600 mt-6">
          Untuk konsultasi hukum lebih lanjut, silakan hubungi <strong>SAP Lawfirm</strong> langsung melalui <a href="https://saplawfirm.com" class="underline hover:text-primary">saplawfirm.com</a>.
        </p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-primary text-white py-6 text-center text-sm">
      <p class="tracking-wide">
        &copy; 2025 Hukum Cerdas — Kolaborasi bersama SAP Lawfirm & Gebukmantan.com
      </p>
    </footer>
  </div>
</template>

<script setup>
import FAQList from '@/components/FAQList.vue';
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 1s ease-out both;
}
.animate-fade-in-up {
  animation: fade-in 1s ease-out both;
  animation-delay: 0.3s;
}
html {
  scroll-behavior: smooth;
}
</style>
