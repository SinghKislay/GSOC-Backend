import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import CardSurface from '../components/CardSurface'

const useStyles = makeStyles(theme => ({
  root: {
    
    flexGrow: 1,
  },
  
}));

export default function AppSurface() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Grid container >
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface/>
      </div>
      </Grid>
      </Grid>
    </div>
  );
}
