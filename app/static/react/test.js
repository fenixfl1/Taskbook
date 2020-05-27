'use strict';

class Main extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="row">

          <div className="card  m-auto" style={{ height: '16rem', width: '14rem' }}>

            <div className="card-header bg-white m-auto">
              <h3 className="m-auto">React js</h3>
            </div>

            <div className="card-body">
              <span className="card-text">Hola mundo</span>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const domContainer = document.querySelector('#root');
ReactDOM.render(<Main />, domContainer);