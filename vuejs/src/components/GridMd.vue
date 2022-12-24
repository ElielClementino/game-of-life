<template>
  <div id="GridMd">
    <div
    class="grid collrows">
    <div
        v-for="(row, rowIndex) in grid"
        :key="rowIndex"
        class="row">
        <div
        v-for="(cell, collIndex) in row"
        :key="collIndex"
        class="cell"
        :style="{
            'background-color': grid[rowIndex][collIndex]
            ? 'rgb(10, 10, 80)'
            : 'rgb(90, 108, 190)'
        }"
        @mousedown="addCell(rowIndex, collIndex)">
        </div>
    </div>
    </div>
    <div class="buttons">
        <button
        :class="running ? 'stop' : 'start'"
        :disabled="!ready"
        @click="alternador()">
        {{ running ? 'Parar' : 'Iniciar'}}
        </button>
    </div>
  </div>
</template>

<script>
export default {
name: 'GridMd',
data () {
  return {
    running: false,
    grid: [],
    COLS: 40,
    ROWS: 40,
    // vizinhos
    neighbors_cells: [
      [-1, -1],
      [-1, 0],
      [-1, 1],
      [0, -1],
      [0, 1],
      [1, -1],
      [1, 0],
      [1, 1]
    ],
    SPEED: 200,
    ready: false
  }
},
mounted () {
  this.seedGrid()
},
methods: {
  cellViva () {
    for (let i = 0; i < this.grid.length; i++) {
      const row = this.grid[i]
      if (row.some(col => col)) {
        this.ready = true
        break
      } else {
        this.ready = false
      }
    }
  },
  alternador () {
    if (this.grid.length && this.ready) {
      this.running = !this.running
      this.runCells()
    }
  },
  runCells () {
    if (this.running) {
      const newGrid = this.grid.map(row => [...row])
      for (let row = 0; row < this.ROWS; row++) {
        for (let col = 0; col < this.COLS; col++) {
          let neighbors = 0
          for (let k = 0; k < this.neighbors_cells.length; k++) {
            const [x, y] = this.neighbors_cells[k]
            const newRow = row + x
            const newCol = col + y
            if (newRow >= 0 && newRow < this.ROWS && newCol >= 0 && newCol < this.COLS) {
              neighbors += this.grid[newRow][newCol]
            }
          }
          if (neighbors < 2 || neighbors > 3) {
            newGrid[row][col] = 0
          } else if (!this.grid[row][col] && neighbors === 3) {
            newGrid[row][col] = 1
          }
        }
      }
      this.grid = newGrid
      setTimeout(this.runCells, this.SPEED)
    }
  },
  gridVazio () {
    this.ready = false
    if (!this.running) {
      this.grid = this.geraGrid(false)
    }
  },
  addCell (row, col) {
    if (!this.running) {
      const newGrid = [...this.grid]
      newGrid[row][col] = this.grid[row][col] ? 0 : 1
      this.grid = newGrid
    }
    this.cellViva()
  },
  geraGrid () {
    const grid = []
    for (let row = 0; row < this.ROWS; row++) {
      grid[row] = []
      for (let col = 0; col < this.COLS; col++) {
        grid[row][col] = 0
      }
    }
    return grid
  },
  seedGrid () {
    if (!this.running) {
      this.grid = this.geraGrid()
      this.ready = true
    }
  }
}
}
</script>

<style>
html, body {
margin: 0;
height: 100%;
background: rgb(141, 139, 210);
background: linear-gradient(159deg, rgba(2,0,36,1) 0%, rgba(9,118,121,1) 44%, rgba(0,212,255,1) 100%);
font-size: 24px;
font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}
.grid {
display: grid;
margin-bottom: 0.5rem;
margin-top: 4rem;
margin-left: 27.5%;
}
.buttons {
display: flex;
justify-content: space-around;
}
button {
margin: 1rem;
cursor: pointer;
padding: 0.5rem;
border-radius: 4px;
border-style: none;
box-shadow: rgba(0, 0, 0, 0.25) 0px 3px 8px;
background-color: rgb(232, 178, 221);
}
button:hover, button:focus, button:active {
box-shadow: rgba(0, 0, 0, 0.50) 0px 3px 8px;
position: relative;
bottom: 2px;
}
.start {
width: 4rem;
background-color: rgb(151, 252, 159);
font-weight: bold;
}
.stop {
width: 4rem;
background-color: rgb(199, 60, 60);
font-weight: bold;
color: white;
}
.collrows {
grid-template-columns: repeat(40, 24px);
grid-template-rows: repeat(40, 16px);
}
.cell {
width: 100%;
height: 100%;
background-color: rgb(195, 167, 167);
cursor: pointer;
}
</style>