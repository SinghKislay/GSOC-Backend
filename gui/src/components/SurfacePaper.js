import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    
  },
  paper: {
    
  }
}));

export default function SurfacePaper() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      
      <Paper className={classes.paper} >
        
      </Paper>
      
    </div>
  );
}
