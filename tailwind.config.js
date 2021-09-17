module.exports = {
  purge: [],
  darkMode: false,
  theme: {
    extend: {
      colors: {
        green: {
          DEFAULT: "#004C54",
        },
        charcoal: {
          DEFAULT: "#565A5C",
        },
        silver: {
          DEFAULT: "#A5ACAF",
        }
      },
      keyframes: {
        animation: {
          logo: "logo 7s infinite"
        },
        logo: {
          "0%": {
            transform: "translate(0px, 0px) scale(1)"
          },
          "33%": {
            transform: "translate(30px, -50px) scale(1.2)"
          },
          "66%": {
            transform: "translate(-20px, 20px) scale(0.8)"
          },
          "100%": {
            transform: "translate(0px, 0px) scale(1)"
          }
        }
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: [],
}
