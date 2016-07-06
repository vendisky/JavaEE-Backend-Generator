import config
import os
from string import upper
from string import lower

currentDir = os.getcwd()



def mkdir(name):
    path = currentDir + '\\' + name
    if not os.path.exists(path):
        os.makedirs(path)
        


def genModel(entity):
    mkdir('model')

    inFile = config.entityDir + '\\' + entity + '.txt'
    outFile = 'model\\' + entity + '.java'
    f = open(outFile, 'w+')

    prefix = """package packageName.model;

public class entity {"""
    prefix = prefix.replace('packageName', config.package)
    prefix = prefix.replace('entity', entity)
    f.write(prefix)
    f.write('\n\n')

    for line in open(inFile):
        l = len(line)
        line = line[0:l-1]
        f.write('\t' + 'private ' + line + ';' + '\n')

    f.write('\n')
    
    getterSetter = """	public attrType getAttrName() {
		return attrName;
	}

	public void setAttrName(attrType attrName) {
		this.attrName = attrName;
	}"""
    for line in open(inFile):
        words = line.split()
        attrType = words[0]
        attrName = words[1]
        AttrName = attrName[0].upper() + attrName[1:]
        
        gsCode = getterSetter.replace('attrType', attrType)
        gsCode = gsCode.replace('attrName', attrName)
        gsCode = gsCode.replace('AttrName', AttrName)

        f.write(gsCode)
        f.write('\n\n')

    f.write('}')

    f.close()



def genDao(entity):
    mkdir('dao')

    outFile = 'dao\\' + entity + 'Dao.java'
    f = open(outFile, 'w+')

    code = """package packageName.dao;

import java.util.List;

import javax.annotation.Resource;

import org.hibernate.SessionFactory;
import org.springframework.orm.hibernate5.support.HibernateDaoSupport;
import org.springframework.stereotype.Repository;

import packageName.model.User;

@Repository
public class UserDao extends HibernateDaoSupport {
	
	@Resource
	public void setMySessionFactory(SessionFactory sessionFactory) {  
        super.setSessionFactory(sessionFactory);  
    }
	
	public User get(Integer userId) {
		return getHibernateTemplate().get(User.class, userId);
	}

	public Integer save(User user) {
		return (Integer) getHibernateTemplate().save(user);
	}

	public void update(User user) {
		getHibernateTemplate().update(user);
	}

	public void delete(User user) {
		getHibernateTemplate().delete(user);
	}

	public void delete(Integer userId) {
		getHibernateTemplate().delete(get(userId));
	}

	public List<User> findAll() {
		String queryStr = "from User";
		return (List<User>) getHibernateTemplate().find(queryStr);
	}
	
}"""

    code = code.replace('packageName', config.package)
    code = code.replace('User', entity)

    entityLower = entity[0].lower() + entity[1:]
    code = code.replace('user', entityLower)

    f.write(code)
    f.close()



def genService(entity):
    mkdir('service')

    outFile = 'service\\' + entity + 'Service.java'
    f = open(outFile, 'w+')

    code = """package packageName.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import packageName.model.User;
import packageName.dao.UserDao;

@Service
public class UserService {

	@Autowired
	private UserDao userDao;

	public User get(Integer userId) {
		return userDao.get(userId);
	}
	
	public Integer save(User user) {
		return userDao.save(user);
	}
	
	public void update(User user) {
		userDao.update(user);
	}
	
	public void delete(User user) {
		userDao.delete(user);
	}
	
	public void delete(Integer userId) {
		userDao.delete(userId);
	}
	
	public List<User> findAll() {
		return userDao.findAll();
	}

}"""

    code = code.replace('packageName', config.package)
    code = code.replace('User', entity)

    entityLower = entity[0].lower() + entity[1:]
    code = code.replace('user', entityLower)

    f.write(code)
    f.close()



def genController(entity):
    mkdir('controller')

    outFile = 'controller\\' + entity + 'Controller.java'
    f = open(outFile, 'w+')
    
    code = """// Not recommended. Need to refer https://www.sitepoint.com/creating-crud-app-minutes-angulars-resource/ and RestController to rewrite it.

package packageName.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import packageName.model.User;
import packageName.service.UserService;

@Controller
public class UserController {
	
	@Autowired
	private UserService userService;

	@RequestMapping(value="/user/{userId}", method=RequestMethod.GET)
	@ResponseBody
	public User get(@PathVariable String userId) {
		User user = userService.get(Integer.valueOf(userId));
		return user;
	}

	@RequestMapping(value="/user", method=RequestMethod.POST)
	@ResponseBody
	public List<User> save(@RequestBody User user) {
		userService.save(user);

		List<User> users = userService.findAll();
		return users;
	}

	@RequestMapping(value="/user/{userId}", method=RequestMethod.PUT)
	@ResponseBody
	public List<User> update(@RequestBody User user) {
		userService.update(user);

		List<User> users = userService.findAll();
		return users;
	}

	@RequestMapping(value="/user/{userId}", method=RequestMethod.DELETE)
	@ResponseBody
	public List<User> delete(@PathVariable String userId) {
		userService.delete(Integer.valueOf(userId));	

		List<User> users = userService.findAll();
		return users;
	}

	@RequestMapping(value="/user", method=RequestMethod.GET)
	@ResponseBody
	public List<User> findAll() { 
		List<User> users = userService.findAll();
		return users;
	}

}"""

    code = code.replace('packageName', config.package)
    code = code.replace('User', entity)

    entityLower = entity[0].lower() + entity[1:]
    code = code.replace('user', entityLower)

    f.write(code)
    f.close()



def genRestController(entity):
    mkdir('controller')

    outFile = 'controller\\' + entity + 'Controller.java'
    f = open(outFile, 'w+')

    code = """package packageName.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import packageName.model.User;
import packageName.service.UserService;

@RestController
public class UserController {
	
	@Autowired
	private UserService userService;

	@RequestMapping(value="/user/{userId}", method=RequestMethod.GET)
	public ResponseEntity<User> get(@PathVariable String userId) {
		User user = userService.get(Integer.valueOf(userId));
		if (user==null) {
			return new ResponseEntity<User>(user, HttpStatus.NOT_FOUND);
		}
		else {
			return new ResponseEntity<User>(user, HttpStatus.OK);
		}
	}

	@RequestMapping(value="/user", method=RequestMethod.POST)
	public ResponseEntity<User> save(@RequestBody User user) {
		Integer userId = userService.save(user);
		User userCreated = userService.get(userId);
		
		return new ResponseEntity<User>(userCreated, HttpStatus.CREATED);
	}

	@RequestMapping(value="/user/{userId}", method=RequestMethod.PUT)
	public ResponseEntity<User> update(@PathVariable String userId, @RequestBody User user) {
		userService.update(user);
		User userUpdated = userService.get(Integer.valueOf(userId));
		return new ResponseEntity<User>(userUpdated, HttpStatus.OK);
	}

	@RequestMapping(value="/user/{userId}", method=RequestMethod.DELETE)
	public ResponseEntity<User> delete(@PathVariable String userId) {
		User userToDelete = userService.get(Integer.valueOf(userId));
		if (userToDelete==null) {
			return new ResponseEntity<User>(userToDelete, HttpStatus.NOT_FOUND);
		}
		else {
			userService.delete(userToDelete);
			return new ResponseEntity<User>(userToDelete, HttpStatus.OK);
		}
	}


	@RequestMapping(value="/user", method=RequestMethod.GET)
	public ResponseEntity<List<User>> findAll() { 
		List<User> users = userService.findAll();
		
		if (users.isEmpty()) {
			return new ResponseEntity<List<User>>(users, HttpStatus.NOT_FOUND);
		}
		else {
			return new ResponseEntity<List<User>>(users, HttpStatus.OK);
		}
	}

}"""

    code = code.replace('packageName', config.package)
    code = code.replace('User', entity)

    entityLower = entity[0].lower() + entity[1:]
    code = code.replace('user', entityLower)

    f.write(code)
    f.close()
    

        
def main():

    for entity in config.entities:
        if config.genModel:
            genModel(entity)
        if config.genDao:
            genDao(entity)
        if config.genService:
            genService(entity)
        if config.genController:
            genController(entity)
        if config.genRestController:
            genRestController(entity)

 

main()
