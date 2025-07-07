#include "Job.h"
#include "Person.h"
#include <drogon/orm/internal/SqlBinder.h>

const std::string Job::Cols::_id = "id";
const std::string Job::Cols::_title = "title";
const std::string Job::primaryKeyName = "id";

Job::Job() :
    id_(nullptr),
    title_(nullptr) {}

void Job::setId(int id)
{
    id_ = &id;
}

void Job::setTitle(const std::string& title)
{
    title_ = &title;
}

int Job::getId() const
{
    return id_;
}

const std::string Job::Cols::title = "title";

void Job::getPersons(const DbClientPtr &clientPtr,
                     const std::function<void(std::vector<Person>)> &rcb,
                     const ExceptionCallback &ecb) const
{
    const static std::string sql = "
