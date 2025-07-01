// src/views/Dashboard.vue
<template>
  <div class="px-6 py-10 min-h-screen bg-gradient-to-b from-gray-50 via-white to-gray-100">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-800 tracking-tight mb-1">Welcome back, <span class="text-primary">Admin</span></h1>
      <p class="text-gray-500 text-sm">Monitor activity and manage legal resources efficiently.</p>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
      <DashboardCard
        title="Questions Asked"
        :value="questionsThisWeek"
        subtitle="This week"
        icon="📝"
        bg="bg-gradient-to-r from-yellow-100 to-yellow-200"
      />
      <DashboardCard
        title="Users per Day"
        :value="usersPerDayAvg"
        subtitle="Daily Average"
        icon="👥"
        bg="bg-gradient-to-r from-blue-100 to-blue-200"
      />
      <DashboardCard
        title="Base Knowledge"
        :value="totalDocuments"
        subtitle="Total Documents"
        icon="📚"
        bg="bg-gradient-to-r from-emerald-100 to-emerald-200"
      />
    </div>

    <!-- Chart Section -->
    <div class="bg-white rounded-2xl shadow-md p-6 mb-10 border border-gray-100">
      <h2 class="text-xl font-semibold text-primary mb-4">Chatbot Responses in the Last 7 Days</h2>
      <div v-if="last7DaysCounts.every(cnt => cnt === 0)" class="text-center text-gray-500 py-16">
        <p class="text-lg font-medium">No activity data available.</p>
      </div>
      <div v-else>
        <canvas id="myChart" height="120"></canvas>
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="bg-white rounded-2xl shadow-md border border-gray-100 p-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">FAQs</h2>
          <p class="text-gray-500 text-sm">Frequently asked legal questions from chatbot sessions</p>
        </div>
        <button
          @click="openModal"
          class="mt-4 sm:mt-0 inline-flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary/90 text-white rounded-md shadow transition"
        >
          <span>➕</span> Add FAQ
        </button>
      </div>

      <div v-if="faqData.length === 0" class="text-center text-gray-500 py-12">
        <p class="text-lg font-medium">No FAQs yet.</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="(item, idx) in faqData"
          :key="idx"
          class="rounded-xl p-5 bg-gradient-to-br from-white to-gray-50 border border-gray-200 shadow-sm hover:shadow-md transition"
        >
          <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ item.question }}</h3>
          <p class="text-sm text-gray-600">{{ item.answer }}</p>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <transition name="modal-fade">
      <div
        v-show="isModalOpen"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50"
      >
        <div class="bg-white rounded-2xl p-8 w-full max-w-lg shadow-xl max-h-[90vh] overflow-y-auto">
          <h2 class="text-xl font-bold text-primary mb-4">Add New FAQ</h2>
          <form @submit.prevent="addFaq" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Question</label>
              <input
                v-model="newFaq.question"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
                placeholder="e.g., Apa itu mafia tanah?"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Answer</label>
              <textarea
                v-model="newFaq.answer"
                rows="4"
                class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
                placeholder="Tuliskan jawaban hukum..."
              ></textarea>
            </div>
            <div class="flex justify-end gap-2 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
              >
                Save FAQ
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>


<script>
import Chart from 'chart.js/auto'
import Swal from 'sweetalert2'
import api from '@/api/axios'
import DashboardCard from '@/components/DashboardCard.vue'

export default {
  components: {
    DashboardCard
  },
  data() {
    return {
      questionsThisWeek: 0,
      usersPerDayAvg: 0,
      totalDocuments: 0,
      chatData: [],
      faqData: [],
      chart: null,
      isModalOpen: false,
      newFaq: { question: '', answer: '' },
      last7DaysLabels: [],
      last7DaysCounts: []
    }
  },
  mounted() {
    this.fetchQuestions();
    this.fetchChatData();
    this.fetchFaqData();
  },
  methods: {
    async fetchQuestions() {
      const { data } = await api.get('/analytics/questions-week')
      this.questionsThisWeek = data.questions_this_week
      const u = await api.get('/analytics/users-average')
      this.usersPerDayAvg = u.data.users_per_day_average
      const d = await api.get('/analytics/docs-total')
      this.totalDocuments = d.data.total_documents
    },
    getLast7DaysLabelsAndDates() {
      const labels = []
      const days = []
      const dayNames = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
      for(let i=6;i>=0;i--) {
        const d = new Date(); d.setDate(d.getDate()-i)
        days.push(d.toISOString().slice(0,10))
        labels.push(dayNames[d.getDay()])
      }
      return { labels, days }
    },
    countMessagesPerDay(data, days) {
      return days.map(day =>
        data.filter(c => c.created_at?.startsWith(day)).length
      )
    },
    async fetchChatData() {
      const res = await api.get('/history')
      this.chatData = res.data
      const { labels, days } = this.getLast7DaysLabelsAndDates()
      this.last7DaysLabels = labels
      this.last7DaysCounts = this.countMessagesPerDay(this.chatData, days)
      if(this.last7DaysCounts.some(c=>c>0)) this.$nextTick(() => this.renderChart())
    },
    renderChart() {
      const ctx = document.getElementById('myChart')
      if(this.chart) this.chart.destroy()
      this.chart = new Chart(ctx, {
        type:'line', data:{ labels:this.last7DaysLabels, datasets:[{ label:'Responses', data:this.last7DaysCounts, borderColor:'#10B981', backgroundColor:'#10B98133', tension:0.4, fill:true }] },
        options:{ responsive:true, plugins:{ legend:{ display:false } }, scales:{ y:{ beginAtZero:true, ticks:{ precision:0 } } } }
      })
    },
    async fetchFaqData() {
      const res = await api.get('/faq')
      this.faqData = res.data
    },
    async addFaq() {
      await api.post('/faq', this.newFaq)
      Swal.fire('Success','FAQ added','success')
      this.fetchFaqData(); this.closeModal()
      this.newFaq={question:'',answer:''}
    },
    openModal(){this.isModalOpen=true},
    closeModal(){this.isModalOpen=false}
  }
}
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity:0; transform:translateY(-20px) }
.modal-fade-enter-to,
.modal-fade-leave-from { opacity:1; transform:translateY(0) }
</style>