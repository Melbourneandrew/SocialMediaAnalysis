<template>
  <div class="menu">
    <!-- Data Menu -->
    <div class="side">
      <h1>Data</h1>
      <div class="menu-inputs">
        <h3>
          Enter some subreddits below. The data from the hot page of these
          forums will be analyzed.
        </h3>
        <div class="subreddits">
          <div
            class="subreddit"
            v-for="(subreddit, index) in subreddits"
            :key="index"
          >
            <h4>r/{{ subreddit }}</h4>
            <v-btn
              class="x-subreddit-btn"
              icon="mdi-close"
              size="x-small"
              variant="outlined"
              @click="removeSubreddit(index)"
            ></v-btn>
          </div>
        </div>
        <v-text-field
          class="subreddit-input"
          v-model="newSubredditField"
          prefix="r/"
          label="Enter subreddit"
          variant="outlined"
        ></v-text-field>
        <v-btn
          class="plus-button"
          icon="mdi-plus"
          @click="addSubreddit"
        ></v-btn>
      </div>
    </div>
    <!-- Analysis selection -->
    <div class="side">
      <h1>Analysis</h1>
      <div class="menu-inputs">
        <h4>
          Select the types of analysis to be run on the data pulled from Reddit
        </h4>
        <p style="text-align: center">(Note that the more analysis you select, the longer it will take to analyze the data)
        </p>
        <div
          class="analysis-option"
          v-for="(option, index) in analysisOptions"
          :key="index"
        >
          <v-checkbox
            v-model="selectedOptions"
            :label="option"
            :value="option"
          ></v-checkbox>
        </div>
        <v-btn
          :loading="responsePending"
          :disabled="responsePending"
          variant="outlined"
          size="large"
          @click="analyze"
        >
          Analyze
        </v-btn>
        <!-- <LoadingBox v-if="showLoading"></LoadingBox> -->
      </div>
    </div>
  </div>
  <div class="output">
    <h1>Output</h1>
    <pre>{{ output }}</pre>
  </div>
</template>

<script setup>
// import LoadingBox from "@/components/LoadingBox.vue";
import { ref } from "vue";

const analysisOptions = ["Emotion", "Hate", "Irony", "Offensive", "Sentiment"];
//all selected by default
const selectedOptions = ref(["Emotion"]);
const subreddits = ref([]);
const newSubredditField = ref("");

function addSubreddit() {
  if (newSubredditField.value === "") return;
  subreddits.value.push(newSubredditField.value);
  newSubredditField.value = "";
}
function removeSubreddit(index) {
  subreddits.value.splice(index, 1);
}

const responsePending = ref(false);
const output = ref(null);
async function analyze() {
  responsePending.value = true;
  if(subreddits.value.length === 0) {
    alert("Please enter at least one subreddit");
    responsePending.value = false;
    return;
  }
  if(selectedOptions.value.length === 0) {
    alert("Please select at least one analysis option");
    responsePending.value = false;
    return;
  }
  const api_url = import.meta.env.VITE_API_URL;
  // convert all entries of selectedOptions to lowercase and remove duplicates
  selectedOptions.value = [...new Set(selectedOptions.value.map((option) => option.toLowerCase()))];
  //convert all entries of subreddits to lowercase and remove duplicates
  subreddits.value = [...new Set(subreddits.value.map((subreddit) => subreddit.toLowerCase()))];

  console.log("Analysis endpoint: ", api_url)
  console.log("Subreddits: ", subreddits.value)
  console.log("Analysis options: ", selectedOptions.value)

  const analysisResponse = await fetch(`${api_url}/a`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      subreddits: subreddits.value,
      analysis_options: selectedOptions.value,
    }),
  });
  responsePending.value = false;
  const res_json = await analysisResponse.json();
  console.log(res_json);

  output.value = JSON.stringify(res_json, null, 2);

}
</script>
<style scoped>
.menu {
  display: flex;
  margin-top: 40px;
  overflow-y: scroll;
}
.side {
  margin: auto;
}
.menu-inputs {
  border-radius: 15px;
  border-width: 2px;
  border-color: black;
  border-style: solid;
  width: 600px;
  height: 600px;
  padding: 20px;
  margin: auto;
}
.subreddit {
  width: 100%;
  border-radius: 5px;
  border-width: 1px;
  border-color: black;
  border-style: solid;
  padding: 10px;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
}
.x-subreddit-btn {
  margin-left: auto;
}
.subreddit-input {
  margin-top: 30px;
}
.plus-button {
  margin-left: 500px;
}

h1,
h3 {
  text-align: center;
}
</style>
