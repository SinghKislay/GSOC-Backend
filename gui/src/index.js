import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {MuiThemeProvider,  responsiveFontSizes, createMuiTheme } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';
//import blueGray from '@material-ui/core/colors/blueGray';

let theme = createMuiTheme({
    palette:{
        type: "dark",
        primary:{
            light: '#607d8b',
            main: '#37474f',
            dark: '#263238',
            
        },

        secondary:{
            light: '#ff9800',
            main: '#fb8c00',
            dark: '#ef6c00',
            
        },
        
        background: {
            default:"#263238",
        },
    },
        
})
theme = responsiveFontSizes(theme);

const Index = () => {
    return(
        
        <MuiThemeProvider theme={theme}>
            <CssBaseline/>
                <App />
        </MuiThemeProvider>
    );
}


ReactDOM.render(<Index />, document.getElementById('root'));
serviceWorker.unregister();
