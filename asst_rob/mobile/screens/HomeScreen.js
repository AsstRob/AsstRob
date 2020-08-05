import React, {useState} from 'react';
import { View, Text, Button, StyleSheet, StatusBar, Picker } from 'react-native';
import { useTheme } from '@react-navigation/native';
// import { Dropdown } from 'react-native-material-dropdown';

const HomeScreen = ({navigation}) => {

  const { colors } = useTheme();

  const theme = useTheme();
  
  const selecedLabel = 0;

  const [count,setCount] = useState(0)
  const show = (value) => {
    if(value == '00') {
      alert("You did't select any device ");
      setCount(value);  

    }
    else {
      alert("You have selected the device " + value);
      setCount(value);
    }
  }
  
    return (
      <View>
      <Picker onValueChange={show.bind()} selectedValue={count}>
        <Picker.Item label="Select a device" value="00"></Picker.Item>
        <Picker.Item label="Device 01" value="01"></Picker.Item>
        <Picker.Item label="Device 02" value="02"></Picker.Item>
      </Picker>
      </View>
    );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    alignItems: 'center', 
    justifyContent: 'center'
  },
});
