/* eslint-disable react-hooks/rules-of-hooks */
/* eslint-disable no-unused-vars */
/* eslint-disable no-alert */
import React, {useState} from 'react';
import {View, Text, Button, StyleSheet, Picker, Image} from 'react-native';
import {createMaterialBottomTabNavigator} from '@react-navigation/material-bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/Ionicons';

const settingsScreen = ({navigation}) => {
  const [count, setCount] = useState(0);
  const show = value => {
    if (value === '00') {
      alert("You did't select any device ");
      setCount(value);
    } else {
      alert('You have selected the device ' + value);
      setCount(value);
    }
  };

  return (
    <View style={styles.container}>
      <Icon.Button
        name="ios-arrow-back"
        size={25}
        backgroundColor="#009387"
        onPress={() => navigation.navigate('HomeDrawer')}
      />
      <Picker onValueChange={show.bind()} selectedValue={count}>
        <Picker.Item label="Select a device" value="00" />
        <Picker.Item label="Device 01" value="01" />
        <Picker.Item label="Device 02" value="02" />
      </Picker>
      <View style={styles.image}>
        <Image resizeMode="center" source={require('../assets/test.png')} />
      </View>
    </View>
  );
};

export default settingsScreen;

const styles = StyleSheet.create({
  container: {
    // justifyContent: 'center',
    // flex: 1,
    // marginTop: 100,
    // alignItems: 'center',
  },
  image: {
    // marginTop: -20,
    alignItems: 'center',
  },
  full: {
    // marginBottom: 200,
  },
});
