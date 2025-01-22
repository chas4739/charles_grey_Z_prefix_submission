
import React, {useState, useEffect} from 'react'
import api from './api'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import ProtectedPage from './Protected';


const App = () => {
  const [items, setItems] = useState([]);
  const [formData, setFormData] = useState({
    userId: '',
    itemName: '',
    itemDescription: '',
    itemQuantity: ''
  });

  const fetchItems = async() => {
    const response = await api.get('/items/');
    setItems(response.data)
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('/items/', formData);
      fetchItems();
      setFormData({
        userId: '',
        itemName: '',
        itemDescription: '',
        itemQuantity: '',
      });
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  function truncateString(str, maxLength) {
    if (str.length <= maxLength) {
      return str;
    } else {
      return str.substring(0, maxLength) + "...";
    }
  }


  return (
  /*     <Router>
      <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/protected" element={<ProtectedPage />} />
      </Routes>
    </Router> */
    
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        <div  className='container-fluid'>
          <a className='navbar-brand' href='#'>
            Inventory App
          </a>
        </div>
      </nav>

      <div className='container'>
        <form onSubmit={handleFormSubmit}>

          <div className = 'mb-3 mt-3'>
            <label htmlFor='userId' className='form-label'>
              User Id 
              <input type='number' className='form-control' id='userId' name='userId' onChange={handleInputChange} value = {formData.userId}/>
            </label>
          </div>

          <div className = 'mb-3'>
            <label htmlFor='itemName' className='form-label'>
              Item Name 
              <input type='text' className='form-control' id='itemName' name='itemName' onChange={handleInputChange} value = {formData.itemName}/>
            </label>
          </div>

          <div className = 'mb-3'>
            <label htmlFor='itemDescription' className='form-label'>
              Item Description 
              <input type='text' className='form-control' id='itemDescription' name='itemDescription' onChange={handleInputChange} value = {formData.itemDescription}/>
            </label>
          </div>

          <div className = 'mb-3'>
            <label htmlFor='itemQuantity' className='form-label'>
              Item Quantity 
              <input type='number' className='form-control' id='itemQuantity' name='itemQuantity' onChange={handleInputChange} value = {formData.itemQuantity}/>
            </label>
          </div>

          <button type = 'submit' className='btn btn-primary'>
            Submit
          </button>

        </form>

        <table className='table table-striped table-bordered table-hover'>
        <thead>
          <tr>
            <th>User Id</th>
            <th>Item Name</th>
            <th>Item Description</th>
            <th>Item Quantity</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.userId}</td>
              <td>{item.itemName}</td>
              <td>{truncateString(item.itemDescription, 100)}</td>
              <td>{item.itemQuantity}</td>
            </tr>
          ))}
        </tbody>
        </table>

      </div>
    </div>
  )

}

export default App
