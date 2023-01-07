module.exports = {
    content: [
        '../**/templates/*.html',
          '../**/templates/**/*.html'
    
    ],
    theme: {
      
      extend: {
        screens: {
          'mxl':{'max':'1279px'},
    
         },
    
        
        animation: {
          fade: 'fade 1s ease-in-out',
          
        },
  
        keyframes: {
          fade: {
            from: {
              opacity: '.4',
            },
            to: {
              opacity: '1',
  
            },
          },
  
        },
      },
    },
    plugins: [],
  }
  