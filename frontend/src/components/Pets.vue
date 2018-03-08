// Pets.vue  // following https://github.com/alessiomaffeis/vue-picture-input-example
<template>
  <div>
    <p>Pets</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button>

    <br><br>
    <picture-input ref="pictureInput" @change="onChange" width="200" height="200" margin="8" accept="image/jpeg,image/png" size="10"
      :removable="true" :customStrings="{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a GIF'
      }">
    </picture-input>


    <p>Pet Name: {{ petName }}</p>
    <button @click="getPetName">Check pet name</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0,
      petName: ""
    }
  },
  methods: {
    getRandom () {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/random`
      axios.get(path)
      .then(response => {
        this.randomNumber = response.data.randomNumber
      })
      .catch(error => {
        console.log(error)
      })
    },

    getPetName () {
      this.petName = this.getPetNameFromBackend()
    },
    getPetNameFromBackend () {
      const path = `http://localhost:5000/api/name`
      axios.get(path)
      .then(response => {
        this.petName = response.data.petName
      })
      .catch(error => {
        console.log(error)
      })
    }



  },
  created () {
    this.getRandom()
    this.getPetName()
  }
}
</script>
