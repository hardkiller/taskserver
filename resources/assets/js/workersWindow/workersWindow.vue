<template>
  <div class="main-window">

    <h5>
       Список исполнителей
       <a class="fa fa-refresh cursor-pointer" @click="getTasksWorkers()"> </a>
     </h5>

    <table class="table">
      <thead>
        <tr>
          <th>Название исполниеля</th>
          <th>Схема</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="worker in taskWorkers">
          <td>{{worker.name}}</td>
          <td>{{worker.json_schema}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {taskWorkers: []}
    },
    methods: {
      getTasksWorkers() {
        axios
          .get("/get_task_workers")
          .then(response => {
            this.taskWorkers = (response.data || []).map((worker) => {

              return {
                name: worker.name,
                json_schema: JSON.stringify(worker.json_schema, null, ' ')
              }
             })
          });
      }
    },
    mounted() {
      this.getTasksWorkers();
    },
    components: {}
  }
</script>