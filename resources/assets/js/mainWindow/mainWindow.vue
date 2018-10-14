<template>
  <div class="main-window">

    <h5>
       История выполнения задач
       <a class="fa fa-refresh cursor-pointer" @click="getTasksResults()"> </a>
     </h5>

    <table class="table">
      <thead>
        <tr>
          <th>Название исполниеля</th>
          <th>Дата начала</th>
          <th>Дата завершения</th>
          <th>Параметры</th>
          <th>Почта</th>
          <th>Результат</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="result in taskResults">
          <td>{{result.task_name}}</td>
          <td>{{result.start_datetime}}</td>
          <td>{{result.end_datetime}}</td>
          <td>{{result.parameters}}</td>
          <td>{{result.email}}</td>
          <td>{{result.result}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {taskResults: []}
    },
    methods: {
      getTasksResults() {
        axios
          .get("/tasks_list")
          .then(response => {
            this.taskResults = response.data
          });
      }
    },
    mounted() {
      this.getTasksResults();
    },
    components: {}
  }
</script>