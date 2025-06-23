<template>
  <div class="landing text-gray-800 scroll-smooth font-sans">

<!-- Hero Section -->
<section
  id="home"
  class="min-h-screen bg-gradient-to-br from-[#f9f6f4] to-white flex items-center px-6 py-20"
>
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
    <!-- Text Content -->
    <div class="text-center md:text-left">
      <h1 class="text-5xl md:text-6xl font-serif font-bold text-neutral-900 leading-tight mb-6">
        AI Chatbot for Land Dispute<br />
        <span class="text-primary">Information & Assistance</span>
      </h1>
      <p class="text-lg text-gray-700 mb-8 leading-relaxed">
        Get access to document-based legal information and case support related to land ownership and <strong>mafia tanah</strong> issues — powered by Retrieval-Augmented Generation and trusted archives from SAP Lawfirm.
      </p>
      <router-link to="/chat">
        <button
          class="inline-flex items-center gap-2 px-8 py-3 bg-primary text-white text-lg font-semibold rounded-md hover:bg-opacity-90 transition-all shadow-md"
        >
          💬 Try Hukum Cerdas
        </button>
      </router-link>
    </div>

    <!-- Hero Image -->
    <div class="relative">
      <div class="hidden md:block">
        <img
          src="@/assets/lawyer-illustration.svg"
          alt="Law Firm Illustration"
          class="w-full h-auto object-cover"
        />
      </div>
    </div>
  </div>
</section>



<!-- About Us Section -->
<section id="about" class="min-h-screen py-24 px-6 bg-white">
  <div class="max-w-7xl mx-auto grid md:grid-cols-2 items-center gap-12">
    <div>
      <h2 class="text-sm font-semibold text-red-700 uppercase tracking-wide mb-2">About the Project</h2>
      <h3 class="text-4xl font-serif font-bold text-neutral-900 mb-6">
        Hukum Cerdas: Legal Access for All
      </h3>
      <p class="text-gray-700 leading-relaxed mb-4">
        Hukum Cerdas is an AI-powered legal assistant developed in collaboration with <strong>SAP Lawfirm</strong> and <strong>Gebukmantan.com</strong> to support legal professionals and the public in understanding and preventing land mafia cases. 
      </p>
      <p class="text-gray-700 leading-relaxed">
        Using Retrieval-Augmented Generation (RAG), this chatbot retrieves trusted legal documents and provides contextual answers without memorizing data — ensuring accuracy, transparency, and compliance.
      </p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <img src="@/assets/office-1.jpg" class="rounded-xl shadow-md w-full h-64 object-cover" />
      <img src="@/assets/office-2.jpg" class="rounded-xl shadow-md w-full h-64 object-cover" />
    </div>
  </div>
</section>



<!-- Features Section -->
<section id="features" class="min-h-screen py-24 px-6 bg-[#f9f6f4]">
  <div class="max-w-7xl mx-auto text-center mb-16">
    <h2 class="text-4xl font-serif font-bold text-neutral-900">Key Capabilities</h2>
    <p class="text-lg text-gray-600 mt-4">Powered by OpenAI/DeepSeek + trusted legal documents from SAP Lawfirm.</p>
  </div>

  <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
    <!-- Feature 1 -->
    <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
      <img src="@/assets/feature-docs.png" alt="Document Retrieval" class="w-full h-64 object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
        <h3 class="text-white text-xl font-semibold mb-2">Document Retrieval</h3>
        <p class="text-sm text-white/80">Find answers from legal sources — no hallucinations, no guesswork.</p>
      </div>
    </div>

    <!-- Feature 2 -->
    <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
      <img src="@/assets/feature-context.png" alt="Context-Aware Responses" class="w-full h-64 object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
        <h3 class="text-white text-xl font-semibold mb-2">Context-Aware Responses</h3>
        <p class="text-sm text-white/80">Answer quality depends on the retrieved content, not memorized data.</p>
      </div>
    </div>

    <!-- Feature 3 -->
    <div class="group relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300">
      <img src="@/assets/feature-247.png" alt="24/7 Availability" class="w-full h-64 object-cover" />
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent p-6 flex flex-col justify-end">
        <h3 class="text-white text-xl font-semibold mb-2">24/7 Availability</h3>
        <p class="text-sm text-white/80">Accessible anytime for public awareness and legal information needs.</p>
      </div>
    </div>
  </div>
</section>



<!-- Call to Action -->
<section class="py-24 bg-primary text-white text-center px-6 relative overflow-hidden">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-4xl md:text-5xl font-serif font-bold mb-6 leading-snug">
      Get Legal Answers<br class="hidden md:block" />Based on Trusted Documents
    </h2>
    <p class="text-lg text-white/90 mb-8">
      Hukum Cerdas uses OpenAI/DeepSeek with RAG to guide you through land disputes, document needs, and public legal resources — not legal advice.
    </p>
    <router-link to="/chat">
      <button class="inline-flex items-center gap-2 px-8 py-3 bg-accent text-primary text-lg font-semibold rounded-md hover:bg-yellow-500 transition shadow-lg">
        💬 Ask Now
      </button>
    </router-link>
  </div>
</section>



<!-- FAQ Section -->
<section id="faq" class="py-24 px-6 bg-white">
  <div class="max-w-5xl mx-auto text-center">
    <h2 class="text-4xl font-serif font-bold text-primary mb-12">Frequently Asked Questions</h2>
    <FAQList />
  </div>
</section>


<!-- Contact Us -->
<section id="contact" class="py-24 px-6 bg-neutralbg">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-4xl font-serif font-bold text-center text-primary mb-12">Get in Touch with Us</h2>
    <form class="grid gap-4 md:grid-cols-2 bg-white p-10 rounded-xl shadow-xl">
      <input
        type="text"
        placeholder="Your Name"
        class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent"
      />
      <input
        type="email"
        placeholder="Your Email"
        class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent"
      />
      <textarea
        rows="4"
        placeholder="Your Message or Feedback"
        class="col-span-2 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-accent"
      ></textarea>
      <button
        type="submit"
        class="col-span-2 bg-primary text-white px-6 py-3 rounded-md hover:bg-opacity-90 transition shadow-md"
      >
        Send Message
      </button>
    </form>
    <p class="text-center text-sm text-gray-600 mt-6">
      For legal consultations, please contact <strong>SAP Lawfirm</strong> directly via <a href="https://saplawfirm.com" class="underline hover:text-primary">saplawfirm.com</a>.
    </p>
  </div>
</section>


<!-- Footer -->
<footer class="bg-primary text-white py-6 text-center text-sm">
  <p class="tracking-wide">
    &copy; 2025 Hukum Cerdas — Built in collaboration with SAP Lawfirm and Gebukmantan.com
  </p>
</footer>


  </div>
</template>

<script setup>
import FAQList from '@/components/FAQList.vue';
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}
</style>
