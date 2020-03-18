import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import CardSurface from '../components/CardSurface'
import DetailCardSurface from '../components/DetailCardSurface'
const useStyles = makeStyles(theme => ({
  root: {
    
    flexGrow: 1,
  },
  
}));

export default function AppSurface() {
  const classes = useStyles();
  const [show, setShow] = useState(false);
  const showAll = (e) => setShow(e)
  return (
    <div className={classes.root}>
      {!show?
      <Grid container >
      <Grid  item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface set={showAll} disease={"pnemonia"} para={para}/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface disease={"Disease2"} para={para}/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface disease={"Disease3"} para={para}/>
      </div>
      </Grid>
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <CardSurface disease={"Disease4"} para={para}/>
      </div>
      </Grid>
      </Grid>
      :
      <Grid container >
      <Grid item xs={12} sm={12} md={6} lg={6}>
      <div style={{marginTop:8}}>
      <DetailCardSurface set={showAll} disease={"pnemonia"} para={para}/>
      </div>
      </Grid>
      </Grid>
      }
    </div>
  );
}

const para = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop."
